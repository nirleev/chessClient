from chessClient import *


def run():
    chess_client = ChessClient()
    chess_client.login()
    chess_client.add_chess_servers()
    chess_client.available_servers()
    chess_client.start_chess_servers_engines()

    # chess_client.parallelize()
    # best_moves = chess_client.get_best_moves()
    chess_client.best_move()
    chess_client.delete_chess_servers()

    chess_client.logout()


if __name__ == "__main__":
    run()
