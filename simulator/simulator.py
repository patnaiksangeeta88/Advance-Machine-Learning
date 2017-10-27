import socket
import random
import time
from collections import deque
random.seed(13)

#-----------------initialization----------------------
width = 6
height = 6
robotLoc = [0, 0]
goalLoc = [width - 1, height - 1]
staticObstacles, dynamicObstacles = [], []
actionQueue = deque(['0','1','2','3','4'])
addObstacles = True
realTimeMode = True
visualization = True
if addObstacles:
    staticObstacles = [[2, 3]]
    dynamicObstacles = [[3, 2],[4,4]]
grid = [['O' for x in range(width)] for y in range(height)]
initialization = [width,height,len(staticObstacles),len(dynamicObstacles)]
# controls = 'sudlr'
controls = '01234'
initialization.extend(robotLoc)
grid[robotLoc[1]][robotLoc[0]] = 'E'
for i in staticObstacles:
    initialization.extend(i)
    grid[i[1]][i[0]] = 'S'
for i in dynamicObstacles:
    initialization.extend(i)
    grid[i[1]][i[0]] = 'Y'
initialization.extend(goalLoc)
grid[goalLoc[1]][goalLoc[0]] = 'G'
#-----------------------open socket----------------------
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 3000)
print ('starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)

connection, client_address = sock.accept()
try:
    # print('connection from', client_address)
    data = connection.recv(2048)
    # print('received "%s"' % data)
    if data:
        init = data.decode('utf-8')
        if init == 'start':
            # print('sending data back to the client')
            connection.sendall(' '.join(str(x) for x in initialization).encode('utf-8'))
        else:
            connection.sendall(b'wrong message')
except socket.error:
    print('No data available')
# finally:
#     # Clean up the connection
#     connection.close()


#---------------------updating functions-------------
def actionFunction(gr, contr, actionQ=False, algo='default'):
    if algo == 'default':
        memo = random.randint(0, len(contr) - 1)
        return contr[memo]
    elif algo == 'client':
        if actionQ:
            return actionQ.popleft()
        else:
            connection, client_address = sock.accept()
            try:
                # print('connection from', client_address)
                data = connection.recv(2048)
                # print('received "%s"' % data)
                print("parse value {}".format(data.decode('utf-8')))
                # if data:
                #     # print('sending data back to the client')
                #     connection.sendall(data)
            except:
                print("No message received.")
            # finally:
            #     # Clean up the connection
            #     connection.close()
    else:
        return


def easyPlot(gr):
    for i in gr:
        print(' '.join(i))
    print('\n')


def updateLocation(gr, ctrs, act, rloc):
    if act == ctrs[0]:
        pass
    elif act == ctrs[1]:
        if rloc[1] > 0:
            rloc[1] -= 1
    elif act == ctrs[2]:
        if rloc[1] < len(gr) - 1:
            rloc[1] += 1
    elif act == ctrs[3]:
        if rloc[0] > 0:
            rloc[0] -= 1
    elif act == ctrs[4]:
        if rloc[0] < len(gr[0]) - 1:
            rloc[0] += 1
    else:
        raise ValueError('Motion operators should be in {}'.format(controls))
    return rloc

#------------------main function---------------------------

easyPlot(grid)
for _ in range(80):
    for i in dynamicObstacles:
        memo = i[:]
        grid[i[1]][i[0]] = 'O'
        action = actionFunction(grid, controls)
        updateLocation(grid, controls, action, i)
        if grid[i[1]][i[0]] in 'YSG':
            i[1], i[0] = memo[1], memo[0]
        elif i == robotLoc:
            print("Hit an obstacle!")
            # easyPlot(grid)
            break
        grid[i[1]][i[0]] = 'Y'

    action = actionFunction(grid, controls, actionQueue, 'client')
    print(action)
    grid[robotLoc[1]][robotLoc[0]] = 'O'
    updateLocation(grid, controls, action, robotLoc)
    grid[robotLoc[1]][robotLoc[0]] = 'E'
    if robotLoc == goalLoc:
        print("Successfully reach the goal!")
        # easyPlot(grid)
        break
    elif robotLoc in staticObstacles or robotLoc in dynamicObstacles:
        print("Hit an obstacle!")
        # easyPlot(grid)
        break

    # if data:
        # print('sending data back to the client')
    connection.sendall(data)

    easyPlot(grid)
    if realTimeMode:
        time.sleep(0.1)
easyPlot(grid)
