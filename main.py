from chessClient import *


def run():
    chess_client = ChessClient()
    chess_client.login()
    # do something
    chess_client.logout()


if __name__ == "__main__":
    run()
