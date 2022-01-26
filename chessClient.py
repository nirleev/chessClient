import sys

from requests import Timeout

from configuration import *
import requests
import json
import asyncio
from websockets import connect
import time
import logging


class ChessClient:
    def __init__(self):
        logging.debug("Init...")
        configuration = Configuration()
        logging.debug("Configuration object created!")
        configuration.read_config()
        logging.debug("Config read!")
        self.config = configuration.get_config()
        logging.debug("Config in a field!")
        self.token = None
        self.main_server = None
        self.stop = False
        self.nodes_searched = {s: 0 for s in self.config["socket_ips"]}
        self.nds_per_sec = {s: 0 for s in self.config["socket_ips"]}
        self.info = {"cp": None, "move": None, "depth": 0, "socket": ""}
        self.time = time.time()
        self.finished = False
        self.input_passed = None
        self.inpt = ""
        self.leave = False
        self.debug = False  # todo to config
        logging.debug("Innit finished!")

    def reset_init(self):
        self.nodes_searched = {s: 0 for s in self.config["socket_ips"]}
        self.nds_per_sec = {s: 0 for s in self.config["socket_ips"]}
        self.info = {"cp": None, "move": None, "depth": 0, "socket": ""}

    def log(self, message):
        if self.debug:
            print(message)

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
                # print(response.text)
                self.log(response.text)
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
            # print(response.text)
            self.log(response.text)
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
                    # print(response.text)
                    self.log(response.text)
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
                # print(response.text)
                self.log(response.text)
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
                    # print(response.text)
                    self.log(response.text)
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
                # print(response.text)
                self.log(response.text)
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
                # print(response.text)
                self.log(response.text)
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
                    try:
                        response = requests.post(url, data=json.dumps(data),
                                                 headers=headers, timeout=2)
                        # print(response.text)
                        self.log(response.text)
                    except Timeout:
                        del self.config['machines_info'][data]

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
                # print(response.text)
                self.log(response.text)
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
                    # print(response.text)
                    self.log(response.text)
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
                    # print(response.text)
                    self.log(response.text)
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
                    # print(response.text)
                    self.log(response.text)
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
                # print(response.text)
                self.log(response.text)
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
                    # print(response.text)
                    self.log(response.text)
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
                    # print(response.text)
                    self.log(response.text)
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
                    # await websocket.send("uci")
                    # while True:
                    #     message = await websocket.recv()
                    #     # print(message)
                    #     if message == 'uciok':
                    #         break

                    await websocket.send("setoption name MultiPV value 1")
                    await websocket.send("isready")
                    while True:
                        message = await websocket.recv()
                        print(message)
                        if message == 'readyok':
                            break

                    # await websocket.send("ucinewgame")
                    await websocket.send("isready")
                    while True:
                        message = await websocket.recv()
                        # print(message)
                        if message == 'readyok':
                            break
                    await websocket.send(f"position startpos moves {self.config['start_pos']}")
                    await websocket.send(f"go {go_options} searchmoves {moves}")

                    info = []
                    while True:
                        await websocket.recv()
                        async for message in websocket:
                            info.append(message)

                            if self.stop is True:
                                await websocket.send("stop")

                            if 'bestmove' in message:
                                # print(f"{socket} --- {info[-2]}")
                                top_moves[info[-2]] = socket
                                return

                            if "info" and "nodes" in message:
                                message = message.split()
                                self.nodes_searched[socket] = int(message[message.index("nodes") + 1])
                                self.nds_per_sec[socket] = int(message[message.index("nps") + 1])
                                mvv = message[message.index("pv") + 1::]
                                cpp = int(message[message.index("cp") + 1])
                                dpth = int(message[message.index("depth") + 1])

                                if self.info["move"] == mvv or self.info["cp"] is None or self.info["cp"] < cpp or \
                                        self.info["socket"] == socket:  # todo more consistent output
                                    self.info["cp"] = cpp
                                    self.info["move"] = mvv
                                    self.info["depth"] = dpth
                                    self.info["socket"] = socket

                                    message[message.index("cp") + 1] = str(cpp)
                                    message[message.index("nodes") + 1] = str(sum(self.nodes_searched.values()))
                                    message[message.index("nps") + 1] = str(sum(self.nds_per_sec.values()))
                                    message[message.index("pv") + 1::] = mvv

                                    print(" ".join(message))  # todo last info same as bestmove??
                                    sys.stdout.flush()



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
            tasks.append(loop.create_task(self.move_eval(url, mvs, top_moves, go_options)))
            prev_step += step
            next += step

        await asyncio.gather(*tasks)

    def parallelize(self, moves, top_moves, go_options):
        asyncio.run(self.distribute_processing(moves, top_moves, go_options))

    async def get_moves(self, go):
        if self.main_server is None:
            self.main_server = self.config['socket_ips'][0]
        if self.token is not None:
            try:
                async with connect(self.main_server,
                                   extra_headers={"Authorization": f"Bearer {self.token}"}) as websocket:
                    # await websocket.send("uci")
                    # while True:
                    #     message = await websocket.recv()
                    #     print(message)
                    #     if message == 'uciok':
                    #         break

                    await websocket.send(f"setoption name MultiPV value {self.config['movesNum']}")
                    await websocket.send("isready")
                    while True:
                        # print(message)
                        message = await websocket.recv()
                        if message == 'readyok':
                            break

                    # await websocket.send("ucinewgame")
                    await websocket.send("isready")
                    while True:
                        message = await websocket.recv()
                        # print(message)
                        if message == 'readyok':
                            break

                    await websocket.send(f"position startpos moves {self.config['start_pos']}")
                    splt = go.split()
                    n_moves = len(self.config['start_pos'].split()) % 2
                    if "btime" in go and n_moves == 1:  # todo ładniej to COŚ TU MOŻE N IE? DZIALAć???
                        tim = int(splt[splt.index("btime") + 1])
                        if tim < 10000:
                            await websocket.send(f"go movetime {tim // 20} depth 10")
                        elif tim < 20000:
                            await websocket.send(f"go movetime {tim // 10} depth 10")
                        elif tim < 40000:
                            await websocket.send(f"go movetime {tim // 5} depth 10")
                        else:
                            await websocket.send(f"go movetime 10000 depth 10")
                    elif "wtime" in go and n_moves == 0:
                        tim = int(splt[splt.index("witme") + 1])
                        if tim < 10000:
                            await websocket.send(f"go movetime {tim // 20} depth 10")
                        elif tim < 20000:
                            await websocket.send(f"go movetime {tim // 10} depth 10")
                        elif tim < 40000:
                            await websocket.send(f"go movetime {tim // 5} depth 10")
                        else:
                            await websocket.send(f"go movetime 10000 depth 10")
                    else:
                        await websocket.send(
                            "go depth 10")  # todo do config | ogranczona ilość ruchów co wtedy??, to głębsze rozbicie BRUH

                    info = []
                    while True:
                        await websocket.recv()
                        async for message in websocket:
                            info.append(message)
                            if time.time() - self.time > 15 or self.stop is True:  # todo to confi?
                                await websocket.send("stop")
                            # print(message)
                            if 'bestmove' in message:

                                multipv = info[-2].split()[info[-2].split().index("multipv") + 1]
                                if self.stop is True:
                                    print(message)
                                    return True, ""

                                # return a list of all moves found with multiPV
                                return False, info[-(int(multipv) + 1):-1]
            except KeyError:
                print("Key error")
            except requests.exceptions.ConnectionError:
                print("Connection error")
        else:
            print("Token is None")

    # get a list of all possible moves in this position (centi-pawn range from best to worst within 100)
    def get_best_moves(self,go):
        leave, strings = asyncio.run(self.get_moves(go))
        if leave:
            return True, ""
        moves_cps = {}
        for move in strings:
            move = move.split()
            moves_cps[move[move.index("pv") + 1]] = move[move.index("cp") + 1]
        best_cp = list(moves_cps.values())[0]

        moves = []
        for cp, move in zip(moves_cps.values(), moves_cps.keys()):
            # filter out bad moves
            if abs(int(best_cp) - int(cp)) > 100 and len(moves) > len(self.config['socket_ips']):
                break
            moves.append(move)

        return False, moves

    def best_move(self, go):
        self.time = time.time()
        leave, moves = self.get_best_moves(go)
        if leave:
            self.stop = False
            return  # todo finish
        top_moves = {}
        off_time = int(time.time() - self.time) * 1000

        times = []
        if "time" in go:
            splt = go.split()
            if "btime" in go:  # todo ładniej to COŚ TU MOŻE N IE? DZIALAć???
                splt[splt.index("btime") + 1] = str(int(splt[splt.index("btime") + 1]) - off_time)
                times.append(int(splt[splt.index("btime") + 1]))
            if "wtime" in go:
                splt[splt.index("wtime") + 1] = str(int(splt[splt.index("wtime") + 1]) - off_time)
                times.append(int(splt[splt.index("btime") + 1]))
            if "movetime" in go:
                splt[splt.index("movetime") + 1] = str(int(splt[splt.index("movetime") + 1]) - off_time)

            go = " ".join(splt)

        go_options = go[3:]

        # time thresholds for moves in a real game
        try:
            for tim in times:
                if tim < 30000:
                    break
            for tim in times:  # todo suboptimal
                if tim < 60000:
                    go_options = "depth 40 movetime 7000"
                elif tim < 120000:
                    go_options = "depth 50 movetime 15000"
                elif tim >= 120000:
                    go_options = "depth 1000 movetime 30000"
        except:
            pass

        self.parallelize(moves, top_moves, go_options)
        self.stop = False
        self.reset_init()
        out = {}
        for move in top_moves.keys():
            move_sp = move.split()
            # retrieve move, cp and socket which found that move
            out[move_sp[move_sp.index("pv") + 1]] = (move_sp[move_sp.index("cp") + 1], top_moves[move], move)

        # dict of moves sorted by cp value, includes url of servers
        out = sorted(out.items(), key=lambda x: int(x[1][0]), reverse=True)
        self.main_server = out[0][1][1]
        self.finished = True
        print(f"bestmove {out[0][0]} ponder ")  # todo
        sys.stdout.flush()
        # print(f"{sum(self.nodes_searched.values())} nodes searched")
        # print(out[0][1][2])

    async def setup_engine(self, socket, options):
        if self.token is not None:
            try:
                async with connect(socket,
                                   extra_headers={"Authorization": f"Bearer {self.token}"}) as websocket:
                    if options != []:
                        for option in options:
                            await websocket.send(option)

                    await websocket.send("isready")
                    while True:
                        message = await websocket.recv()
                        if message == 'readyok':
                            break

                    await websocket.send("ucinewgame")
                    await websocket.send("isready")
                    while True:
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

    # user options relayed to every engine --
    def setup_engines(self, options):
        asyncio.run(self.send_options(options))
