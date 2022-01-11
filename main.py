from chessClient import *


def run():
    #todo stin loop, iready impementation, setoption gathering, relay position/time/depth limits
    chess_client = ChessClient()
    chess_client.login()
    chess_client.add_chess_servers()
    chess_client.available_servers()
    chess_client.start_chess_servers_engines()
    chess_client.setup_enginess()
    chess_client.best_move()
    chess_client.delete_chess_servers()

    chess_client.logout()


if __name__ == "__main__":
    run()
