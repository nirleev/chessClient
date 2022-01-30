import logging

logging.basicConfig(filename="mylog.log", level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


logging.debug("Importing...")

import sys
from chessClient import *
import threading

logging.debug("Creating Chess Client...")
chess_client = ChessClient()
logging.debug("Chess Client created!")


def run():
    print("Parallel Uci engine")
    logging.debug("Parallel Uci engine")
    sys.stdout.flush()

    if chess_client.login() is None:
        print("Invalid credentials")
        logging.debug("Invalid credentials")

    else:
        chess_client.add_chess_servers()
        logging.debug("Adding servers...")
        chess_client.available_servers()
        logging.debug("checking servers' availability...")
        chess_client.start_chess_servers_engines()
        logging.debug("Starting servers...")
        uci_response = """id name Parallel
id author :)

option name Debug Log File type string default
option name Threads type spin default 1 min 1 max 512
option name Hash type spin default 16 min 1 max 33554432
option name Clear Hash type button
option name Skill Level type spin default 20 min 0 max 20
option name Move Overhead type spin default 10 min 0 max 5000
option name Slow Mover type spin default 100 min 10 max 1000
option name nodestime type spin default 0 min 0 max 10000
option name UCI_Chess960 type check default false
option name UCI_AnalyseMode type check default false
option name UCI_LimitStrength type check default false
option name UCI_Elo type spin default 1350 min 1350 max 2850
option name UCI_ShowWDL type check default false
option name SyzygyPath type string default <empty>
option name SyzygyProbeDepth type spin default 1 min 1 max 100
option name Syzygy50MoveRule type check default true
option name SyzygyProbeLimit type spin default 7 min 0 max 7
option name Use NNUE type check default true
uciok"""

        options = []
        while True:
            if chess_client.input_passed is None:
                chess_client.inpt = input()
                logging.debug(f"INPUT === {chess_client.inpt}")
                chess_client.log(f"INPUT === {chess_client.inpt}")
            elif chess_client.input_passed is False:
                chess_client.inpt = ""
            elif chess_client.input_passed is True:
                chess_client.input_passed = None

            if 'uci' == chess_client.inpt:
                print(uci_response)
                logging.debug(uci_response)
            elif 'isready' in chess_client.inpt:
                print('readyok')
            elif 'setoption' and 'MultiPV' in chess_client.inpt:
                pass
            elif 'setoption' in chess_client.inpt:
                options.append(chess_client.inpt)
                chess_client.setup_engines(options)
            elif 'ucinewgame' in chess_client.inpt:
                pass
            elif 'position' in chess_client.inpt:
                chess_client.config['start_pos'] = " ".join(chess_client.inpt.split()[3:])
                chess_client.log(f"POSITION ===== {chess_client.config['start_pos']}")
            elif 'go' in chess_client.inpt:
                t1 = threading.Thread(target=chess_client.best_move, args=(chess_client.inpt,))
                t2 = threading.Thread(target=stop)

                t1.start()
                t2.start()

                t1.join()
                t2.join()
            elif 'quit' in chess_client.inpt:
                chess_client.stop = True
                chess_client.leave = True
                chess_client.input_passed = True

            if chess_client.leave is True:
                break
            chess_client.log("LOOP DONE")
            sys.stdout.flush()

        chess_client.stop_chess_servers_engines()
        chess_client.delete_chess_servers()
        chess_client.logout()


def stop():
    chess_client.finished = False
    chess_client.input_passed = False
    while True:
        chess_client.inpt = input()
        print(f"INPUT2 === {chess_client.inpt}")
        logging.debug(f"INPUT2 === {chess_client.inpt}")
        if 'stop' in chess_client.inpt:
            chess_client.stop = True
            chess_client.leave = False
            chess_client.input_passed = True
            return
        elif 'quit' in chess_client.inpt:
            chess_client.stop = True
            chess_client.leave = True
            chess_client.input_passed = True
            return
        elif chess_client.finished is True:
            chess_client.finished = False
            chess_client.input_passed = True
            print("FINISHED")
            return


if __name__ == "__main__":
    run()