from stockfish import Stockfish
from configuration import *
from multiprocessing import Process

configuration = Configuration()
configuration.read_config()
config = configuration.get_config()


def best_moves_depth(moves, depth, start_pos):
    engine = Stockfish(config["engine_location"], parameters={"MultiPV": config['machines']})
    engine.set_depth(depth)
    engine.set_position(start_pos)
    return engine.get_top_moves(moves)


def best_moves_time(self, moves, time, start_pos):
    engine = Stockfish(config["engine_location"], parameters={"MultiPV": config['machines']})
    engine.set_position(start_pos)
    return engine.get_top_moves_time(moves, time=time)


def just_run(tokens, config, bestmoves):
    best_moves_time(config['machines'] * 2, config['main_time'], config['start_pos'])

    nodes = []
    for item, (token, bmovess) in enumerate(zip(tokens, bestmoves)):
        nodes.append(Process(target=talk, args=(
        f"{config['socket_ips'][0]}/ws_engine", 2, config['start_pos'][item] + ' ' + bmovess, token)))

    parallel_run(nodes)


def parallel_run(*ins):
    proc = []
    for p in ins:
        for pp in p:
            pp.start()
            proc.append(pp)
    for p in proc:
        p.join()


if __name__ == "__main__":
    best_moves = best_moves_depth(config['machines'], config['depth'], config['start_pos'])
    best_moves1 = [m['Move'] for m in reversed(best_moves)]
    print(best_moves)

    best_moves = best_moves_depth(config['machines'] * 2, config['depth'], config['start_pos'])
    print(best_moves)

    # tokens = get_tokens(config)
    # just_run(tokens, config, best_moves1)
