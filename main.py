from chessClient import *
import threading

leave = False
chess_client = ChessClient()
inpt = ""
finished = False

def run():
    if chess_client.login() is None:
        print("Invalid credentials")
    else:
        chess_client.add_chess_servers()
        chess_client.available_servers()
        chess_client.start_chess_servers_engines()
        uci_response = """option name Debug Log File type string default
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
option name EvalFile type string default nn-3475407dc199.nnue"""  # todo to config?

        options = []
        while True:
            if finished is False:
                inpt = input()
                finished = False
            print('XXDD')
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
                chess_client.config['start_pos'] = " ".join(inpt.split()[3:])
            elif 'go' in inpt:
                chess_client.setup_engines(options)
                t1 = threading.Thread(target=chess_client.best_move, args=(inpt,))
                t2 = threading.Thread(target=stop)
                # chess_client.start_chess_servers_engines()
                # chess_client.best_move(inpt)
                t1.start()
                t2.start()

                t1.join()
                t2.join()
                print('bruh')

            if leave is True:
                break

        chess_client.stop_chess_servers_engines()
        chess_client.delete_chess_servers()
        chess_client.logout()


def stop():
    while True:
        inpt = input()
        if 'stop' in inpt:  # todo use some http methods????
            chess_client.stop = True
            leave = False
            return
        elif 'quit' in inpt:
            chess_client.stop = True
            chess_client.stop_chess_servers_engines()
            leave = True
            return
        elif chess_client.finished is True:
            chess_client.finished = False
            finished = True
            return


if __name__ == "__main__":
    run()
