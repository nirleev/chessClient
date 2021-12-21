from chessClient import *


def run():
    chess_client = ChessClient()
    chess_client.login()
    chess_client.add_chess_servers()
    chess_client.available_servers()
    chess_client.start_chess_servers_engines()#tu się wywala
    chess_client.setup_engines()


    # do something
    chess_client.logout()


if __name__ == "__main__":
    run()
