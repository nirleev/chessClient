from chessClient import *


def run():
    uci_response = 'blebleblebel'
    #todo stin loop, isready impementation, setoption gathering, relay position/time/depth limits
    chess_client = ChessClient()
    chess_client.login()
    chess_client.add_chess_servers()
    chess_client.available_servers()
    chess_client.start_chess_servers_engines()
    options = []
    go = ''
    while True:
        inpt = input()
        if 'uci' in inpt:
            print(uci_response)
        elif 'isready' in inpt:
            print('readyok')
        elif 'setoption' in inpt:
            options.append(inpt)
        elif 'position' in inpt:
            config['start_pos'] = " ".join(inpt.split()[3:])
            print(config['start_pos'])
        elif 'go' in inpt:
            go = inpt
            break#todo go somehow

    chess_client.setup_engines(options)
    chess_client.best_move()
    chess_client.delete_chess_servers()

    # do something
    chess_client.logout()


if __name__ == "__main__":
    run()
