from trainer import *



if __name__ == "__main__":
    timeframe = 0.5
    parser = argparse.ArgumentParser(description='Start a simulator training server.')
    parser.add_argument('-s', '--seed', action='store', dest='seed', default='', help='Import seed for random numbers')
    parser.add_argument('-p', '--plot', action='store_true', dest='plot', default=False, help='Turn on simple plot')
    parser.add_argument('-c', '--constant', action='store', dest='constant', help='input constant')
    parser.add_argument('-row', action='store', dest='row', default='6', help='Import row size for grid')
    parser.add_argument('-col', action='store', dest='col', default='6', help='Import row size for grid')
    parser.add_argument('-sta', action='store', dest='sta', default='2',
                        help='Import number of static obstacles for grid')
    parser.add_argument('-dyn', action='store', dest='dyn', default='2',
                        help='Import number of dynamic obstacles for grid')
    args = parser.parse_args()
    PRINTOUT = vars(args)['plot']
    SEEDED = vars(args)['seed']
    ROW = int(vars(args)['row'])
    COL = int(vars(args)['col'])
    STA = int(vars(args)['sta'])
    DYN = int(vars(args)['dyn'])

    if SEEDED:
        random.seed(int(SEEDED))
    #set Grid parameters in the next line. Grid(10,10,5,3) means 10 by 10 map with 5 static and 3 dynamic obstacles
    game = Grid(ROW, COL, STA, DYN)
    if PRINTOUT:
        game.simplePlot()
    connection = createSocket(4000)
    data = connection.recv(2048).decode("utf-8")
    if data == "start":
        connection.sendall(game.dump('init').encode("utf-8"))


    while True:
        if not game.agent.actionQueue:
            data = connection.recv(2048).decode("utf-8")
            game.agent.fetchActions(data)

        if game.win == 1:
            if PRINTOUT:
                print("win")
            connection.sendall("win".encode("utf-8"))
            break
        elif game.win == -1:
            if PRINTOUT:
                print("lose")
            connection.sendall("lose".encode("utf-8"))
            break
        elif game.win == 0:
            connection.sendall(game.dump().encode("utf-8"))

        game.updateAll()
        if PRINTOUT:
            game.simplePlot()
