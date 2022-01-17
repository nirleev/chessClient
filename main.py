from chessClient import *


def run():
    chess_client = ChessClient()
    chess_client.login()
    chess_client.add_chess_servers()
    chess_client.available_servers()
    chess_client.start_chess_servers_engines()
    uci_response = 'blebleblebel'
    options = []
    while True:
        inpt = input()
        if 'uci' == inpt:
            print(uci_response)  # todo implement response
        elif 'isready' in inpt:
            print('readyok')
        elif 'setoption' and 'MultiPV' in inpt:
            pass
        elif 'setoption' in inpt:
            options.append(inpt)
        # ignoring MultiPV for now
        elif 'ucinewgame' in inpt:
            pass
        elif 'position' in inpt:
            config['start_pos'] = " ".join(inpt.split()[3:])
            print(config['start_pos'])
        elif 'go' in inpt:
            print(chess_client.best_move(inpt))
        elif 'stop' in inpt:  # todo stop implementation
            chess_client.stop = True
        elif 'quit' in inpt:
            break

        if options != []:
            chess_client.setup_engines(options)
            options = []

    chess_client.delete_chess_servers()
    chess_client.logout()


if __name__ == "__main__":
    run()
