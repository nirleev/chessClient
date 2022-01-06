from config import config
import requests
import json
import asyncio
from websockets import connect
from multiprocessing import Process


class ChessClient:
    def __init__(self):
        self.token = None

    ''' USER METHODS '''

    # POST /user/add
    def add_user(self):
        headers = {'Authorization': f'Bearer {self.token}', 'Content-type': 'application/json'}
        try:
            for info in config['users']:
                data = {
                    "login": info["login"],
                    "password": info["password"]
                }

                url = f"{config['uciServer']}/user/add"
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
                "login": config["login"],
                "password": config["password"]
            }
            url = f"{config['uciServer']}/user/login"

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
            url = f"{config['uciServer']}/user/logout"
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
                url = f"{config['uciServer']}/engine/add"
                for data in config['engines']:
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
                url = f"{config['uciServer']}/engine/available"
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
                url = f"{config['uciServer']}/engine/send"
                for command in config['commands']:
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
                    'name': config['engine']
                }
                url = f"{config['uciServer']}/engine/start"
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
                url = f"{config['uciServer']}/engine/stop"
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
                url = f"{config['uciServer']}/server/add"
                for data in config['machines_info']:
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
                url = f"{config['uciServer']}/server/all"
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
                url = f"{config['uciServer']}/server/command"
                for command in config['commands_servers']:
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
                url = f"{config['uciServer']}/server/command-engine"
                for command in config['commands_engines']:
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
                url = f"{config['uciServer']}/server/delete"
                for data in config['delete_machines']:
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
                url = f"{config['uciServer']}/server/heartbeat"
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
                for info in config['machines_info']:
                    data = {
                        'engineName': config["engine"],
                        'serverName': info["name"]
                    }

                    url = f"{config['uciServer']}/server/start-engine"
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
                for info in config['machines_info']:
                    url = f"{config['uciServer']}/server/stop-engine"
                    response = requests.post(url, data=info["name"], headers=headers)
                    print(response.text)
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    ''' WEBSOCKETS COMMUNICATION '''

    async def move_eval(self, socket, moves):
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
                    await websocket.send(f"position startpos moves {config['movesNum']}")
                    await websocket.send(f"go movetime 15000 searchmoves {moves}")

                    info = []
                    while True:
                        await websocket.recv()
                        async for message in websocket:
                            info.append(message)
                            print(message)
                            if 'bestmove' in message:
                                print(f"this --- {info[-2]}")
                                return info[-2]
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    # https://stackoverflow.com/questions/49858021/listen-to-multiple-socket-with-websockets-and-asyncio
    async def distibute_processing(self, moves):
        loop = asyncio.get_event_loop()
        tasks = []
        prev_step = 0
        step = len(moves) // len(config['socket_ips'])
        next = step
        for engine, url in enumerate(config['socket_ips']):
            mvs = ''
            for m in moves[prev_step:next]:
                mvs += f"{m} "
                #todo may go out of bouds or not take a move into account?
            tasks.append(loop.create_task(self.move_eval(url, mvs)))
            prev_step += step
            next += step

        await asyncio.gather(*tasks)

    def parallelize(self, moves):
        asyncio.run(self.distibute_processing(moves))

    async def get_moves(self, socket=None):
        if socket is None:
            socket = config['socket_ips'][0]
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

                    await websocket.send(f"setoption name MultiPV value {config['movesNum']}")
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

                    await websocket.send(f"position startpos moves {config['movesNum']}")
                    await websocket.send("go depth 10")

                    info = []
                    while True:
                        await websocket.recv()
                        async for message in websocket:
                            info.append(message)
                            print(message)
                            if 'bestmove' in message:
                                print(info[-(config['movesNum'] + 1):-1])
                                return info[-(config['movesNum'] + 1):-1]
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    def get_best_moves(self, socket=None):
        strings = asyncio.run(self.get_moves(socket))
        moves_cps = {}
        for move in strings:
            moves_cps[move.split()[21]] = move.split()[9]
        best_cp = list(moves_cps.values())[0]

        moves = []
        for cp, move in zip(moves_cps.values(), moves_cps.keys()):
            if abs(int(best_cp) - int(cp)) > 100 and len(moves) > len(config['socket_ips']):
                break
            moves.append(move)

        return moves

    def best_move(self):
        moves = self.get_best_moves()
        self.parallelize(moves)
