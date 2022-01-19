from configuration import *
import requests
import json
import asyncio
from websockets import connect
from multiprocessing import Process


class ChessClient:
    def __init__(self):
        configuration = Configuration()
        configuration.read_config()
        self.config = configuration.get_config()
        self.token = None
        self.main_server = None
        self.stop = False  # todo implement stopping while searching for the best move
        self.nodes_searched = {s: 0 for s in self.config["socket_ips"]}  # todo test this

    ''' USER METHODS '''

    # POST /user/add
    def add_user(self):
        headers = {'Authorization': f'Bearer {self.token}', 'Content-type': 'application/json'}
        try:
            for info in self.config['users']:
                data = {
                    "login": info["login"],
                    "password": info["password"]
                }

                url = f"{self.config['uciServer']}/user/add"
                response = requests.post(url, data=json.dumps(data), headers=headers)
                print(response.text)
        except KeyError:
            print("Key error")
        except requests.exceptions.ConnectionError:
            print("Connection error")

    # POST /user/login
    def login(self):
        headers = {'Content-type': 'application/json'}
        try:
            data = {
                "login": self.config["login"],
                "password": self.config["password"]
            }
            url = f"{self.config['uciServer']}/user/login"

            response = requests.post(url, data=json.dumps(data), headers=headers)
            resp = json.loads(response.text)
            self.token = resp["token"]
        except KeyError:
            print("Key error")
        except requests.exceptions.ConnectionError:
            print("Connection error")

        return self.token

    # POST /user/logout
    def logout(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        try:
            url = f"{self.config['uciServer']}/user/logout"
            response = requests.post(url, headers=headers)
            print(response.text)
        except KeyError:
            print("Key error")
        except requests.exceptions.ConnectionError:
            print("Connection error")

    ''' ENGINE METHODS '''

    # POST /engine/add (adds all chess engines from config)
    def add_engines(self):
        if self.token is not None:
            headers = {'Authorization': f'Bearer {self.token}', 'Content-type': 'application/json'}
            try:
                url = f"{self.config['uciServer']}/engine/add"
                for data in self.config['engines']:
                    response = requests.post(url, data=json.dumps(data), headers=headers)
                    print(response.text)
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    # POST /engine/available
    def available_engines(self):
        if self.token is not None:
            headers = {'Authorization': f'Bearer {self.token}'}
            try:
                url = f"{self.config['uciServer']}/engine/available"
                response = requests.get(url, headers=headers)
                print(response.text)
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    # POST /engine/send
    def send_command_to_engine(self):
        if self.token is not None:
            headers = {'Authorization': f'Bearer {self.token}'}
            try:
                url = f"{self.config['uciServer']}/engine/send"
                for command in self.config['commands']:
                    response = requests.post(url, data=command, headers=headers)
                    print(response.text)
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    # POST /engine/start
    def start_uci_server_engine(self):
        if self.token is not None:
            headers = {'Authorization': f'Bearer {self.token}', 'Content-type': 'application/json'}
            try:
                data = {
                    'name': self.config['engine']
                }
                url = f"{self.config['uciServer']}/engine/start"
                response = requests.post(url, data=json.dumps(data), headers=headers)
                print(response.text)
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    # POST /engine/stop
    def stop_uci_server_engine(self):
        if self.token is not None:
            headers = {'Authorization': f'Bearer {self.token}', 'Content-type': 'application/json'}
            try:
                url = f"{self.config['uciServer']}/engine/stop"
                response = requests.post(url, headers=headers)
                print(response.text)
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    ''' SERVER METHODS '''

    # POST /server/add (adds all Chess Servers from config)
    def add_chess_servers(self):
        if self.token is not None:
            headers = {'Authorization': f'Bearer {self.token}', 'Content-type': 'application/json'}
            try:
                url = f"{self.config['uciServer']}/server/add"
                for data in self.config['machines_info']:
                    response = requests.post(url, data=json.dumps(data), headers=headers)
                    print(response.text)
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    # GET /server/all
    def available_servers(self):
        if self.token is not None:
            headers = {'Authorization': f'Bearer {self.token}'}
            try:
                url = f"{self.config['uciServer']}/server/all"
                response = requests.get(url, headers=headers)
                print(response.text)
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    # POST /server/command
    def send_command_to_servers(self):
        if self.token is not None:
            headers = {'Authorization': f'Bearer {self.token}'}
            try:
                url = f"{self.config['uciServer']}/server/command"
                for command in self.config['commands_servers']:
                    response = requests.post(url, data=command, headers=headers)
                    print(response.text)
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    # POST /server/command-engine
    def send_command_to_engine_on_servers(self):
        if self.token is not None:
            headers = {'Authorization': f'Bearer {self.token}'}
            try:
                url = f"{self.config['uciServer']}/server/command-engine"
                for command in self.config['commands_engines']:
                    response = requests.post(url, data=command, headers=headers)
                    print(response.text)
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    # POST /server/delete (delete all Chess Servers from config)
    def delete_chess_servers(self):
        if self.token is not None:
            headers = {'Authorization': f'Bearer {self.token}'}
            try:
                url = f"{self.config['uciServer']}/server/delete"
                for data in self.config['delete_machines']:
                    response = requests.post(url, data=data['name'], headers=headers)
                    print(response.text)
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    # GET /server/heartbeat
    def check_connections(self):
        if self.token is not None:
            headers = {'Authorization': f'Bearer {self.token}'}
            try:
                url = f"{self.config['uciServer']}/server/heartbeat"
                response = requests.get(url, headers=headers)
                print(response.text)
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    # POST /server/start-engine (starts all Chess Servers from config)
    def start_chess_servers_engines(self):
        if self.token is not None:
            headers = {'Authorization': f'Bearer {self.token}', 'Content-type': 'application/json'}
            try:
                for info in self.config['machines_info']:
                    data = {
                        'engineName': self.config["engine"],
                        'serverName': info["name"]
                    }

                    url = f"{self.config['uciServer']}/server/start-engine"
                    response = requests.post(url, data=json.dumps(data), headers=headers)
                    print(response.text)
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    # POST /server/stop-engine (stops engines for all Chess Servers from config)
    def stop_chess_servers_engines(self):
        if self.token is not None:
            headers = {'Authorization': f'Bearer {self.token}'}
            try:
                for info in self.config['machines_info']:
                    url = f"{self.config['uciServer']}/server/stop-engine"
                    response = requests.post(url, data=info["name"], headers=headers)
                    print(response.text)
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    ''' WEBSOCKETS COMMUNICATION '''

    async def move_eval(self, socket, moves, top_moves, go_options):
        if self.token is not None:
            try:
                async with connect(socket,
                                   extra_headers={"Authorization": f"Bearer {self.token}"}) as websocket:
                    await websocket.send("uci")
                    while True:
                        message = await websocket.recv()
                        print(message)
                        if message == 'uciok':
                            break

                    await websocket.send("setoption name MultiPV value 1")
                    await websocket.send("isready")
                    while True:
                        print(message)
                        message = await websocket.recv()
                        if message == 'readyok':
                            break

                    await websocket.send("ucinewgame")
                    await websocket.send("isready")
                    while True:
                        message = await websocket.recv()
                        print(message)
                        if message == 'readyok':
                            break
                    await websocket.send(f"position startpos moves {self.config['start_pos']}")
                    await websocket.send(f"go {go_options} searchmoves {moves}")

                    info = []
                    while True:
                        await websocket.recv()
                        async for message in websocket:
                            info.append(message)
                            print(message)
                            if 'bestmove' in message:
                                print(f"{socket} --- {info[-2]}")
                                top_moves[info[-2]] = socket
                                return
                            elif 'nodes' in message:
                                message = message.split()
                                self.nodes_searched[socket] = int(message[message.index("nodes") + 1])
                        if self.stop is True:
                            await websocket.send("stop")  # todo sending too many times may break something??????
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    # https://stackoverflow.com/questions/49858021/listen-to-multiple-socket-with-websockets-and-asyncio
    async def distribute_processing(self, moves, top_moves, go_options):
        loop = asyncio.get_event_loop()
        tasks = []
        prev_step = 0
        step = len(moves) // len(self.config['socket_ips'])
        next = step
        for engine, url in enumerate(self.config['socket_ips']):
            mvs = ''
            for m in moves[prev_step:next]:
                mvs += f"{m} "
                # todo may go out of bouds or not take a move into account?
            tasks.append(loop.create_task(self.move_eval(url, mvs, top_moves, go_options)))
            prev_step += step
            next += step

        await asyncio.gather(*tasks)

    def parallelize(self, moves, top_moves, go_options):
        asyncio.run(self.distribute_processing(moves, top_moves, go_options))

    async def get_moves(self):
        if self.main_server is None:
            self.main_server = self.config['socket_ips'][0]
        if self.token is not None:
            try:
                async with connect(self.main_server,
                                   extra_headers={"Authorization": f"Bearer {self.token}"}) as websocket:
                    await websocket.send("uci")
                    while True:
                        message = await websocket.recv()
                        print(message)
                        if message == 'uciok':
                            break

                    await websocket.send(f"setoption name MultiPV value {self.config['movesNum']}")
                    await websocket.send("isready")
                    while True:
                        print(message)
                        message = await websocket.recv()
                        if message == 'readyok':
                            break

                    await websocket.send("ucinewgame")
                    await websocket.send("isready")
                    while True:
                        message = await websocket.recv()
                        print(message)
                        if message == 'readyok':
                            break

                    await websocket.send(f"position startpos moves {self.config['start_pos']}")
                    await websocket.send("go depth 10")

                    info = []
                    while True:
                        await websocket.recv()
                        async for message in websocket:
                            info.append(message)
                            print(message)
                            if 'bestmove' in message:
                                # return a list of all moves found with multiPV
                                multipv = info[-2].split()[info[-2].split().index("multipv") + 1]
                                print(info[-(int(multipv) + 1):-1])
                                return info[-(int(multipv) + 1):-1]
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    # get a list of all possible moves in this position (centi-pawn range from best to worst within 100)
    def get_best_moves(self):
        strings = asyncio.run(self.get_moves())
        moves_cps = {}
        for move in strings:
            moves_cps[move.split()[21]] = move.split()[9]
        best_cp = list(moves_cps.values())[0]

        moves = []
        for cp, move in zip(moves_cps.values(), moves_cps.keys()):
            # filter out bad moves
            if abs(int(best_cp) - int(cp)) > 100 and len(moves) > len(self.config['socket_ips']):
                break
            moves.append(move)

        return moves

    def best_move(self, go):
        moves = self.get_best_moves()
        top_moves = {}
        go_options = go[3:]
        self.parallelize(moves, top_moves, go_options)
        out = {}
        for move in top_moves.keys():
            move_sp = move.split()
            # retrieve move, cp and socket which found that move
            out[move_sp[move_sp.index("pv") + 1]] = (move_sp[move_sp.index("cp") + 1], top_moves[move], move)

        # dict of moves sorted by cp value, includes url of servers
        out = sorted(out.items(), key=lambda x: int(x[1][0]), reverse=True)
        self.main_server = out[0][1][1]
        self.stop = False
        print(out[0][0])
        print(f"{sum(self.nodes_searched.values())} nodes searched")
        print(out[0][1][2])

    async def setup_engine(self, socket, options):
        if self.token is not None:
            try:
                async with connect(socket,
                                   extra_headers={"Authorization": f"Bearer {self.token}"}) as websocket:
                    await websocket.send("uci")
                    while True:
                        message = await websocket.recv()
                        print(message)
                        if message == 'uciok':
                            break

                    for option in options:
                        await websocket.send(option)

                    await websocket.send("isready")
                    while True:
                        print(message)
                        message = await websocket.recv()
                        if message == 'readyok':
                            break

            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    async def send_options(self, options):
        loop = asyncio.get_event_loop()
        tasks = []
        for socket in self.config['socket_ips']:
            tasks.append(loop.create_task(self.setup_engine(socket, options)))

        await asyncio.gather(*tasks)

    # user options relayed to every engine -- todo implementation for certain options ex. multipv??
    def setup_engines(self, options):
        asyncio.run(self.send_options(options))

    # todo correct output printed
