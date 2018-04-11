import datetime
import socket
import time

from communication.decoders import Decoder
from communication.encoders import Encoder
from communication.opcodes import *
from server.engine import Engine


class GameServer:
    def __init__(self, host, port, fps=60):
        self.host = host
        self.port = port
        self.server = None
        self.fps = fps
        self.frame_time = 1 / fps * 1000000
        self.clients = []
        self.server = None
        self.engine = None
        self.players = None

    def connect(self, players=2):
        self.players = players
        self.engine = Engine(players=self.players)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(players)

        for x in range(players):
            (client, address) = self.server.accept()
            self.clients.append((client, address))
            client.sendall(Encoder.encode_string(str(Engine.HEIGHT) + 'x' + str(Engine.WIDTH)))

    def update(self):
        while True:
            frame_start = datetime.datetime.now()
            objects, lives, scores = self.engine.update()
            if len(objects) == 0:
                order = []
                v = [x for x in range(self.players)]
                v = sorted(v, key=lambda k:self.engine.scores[k], reverse=True)

                for x in range(self.players):
                    self.clients[v[x]][0].sendall(Encoder.encode_int(0))
                    self.clients[v[x]][0].sendall(Encoder.encode_int(int(self.engine.scores[v[x]])))
                    self.clients[v[x]][0].sendall(Encoder.encode_int(x+1))
                time.sleep(3)
                self.engine = Engine(players=self.players)
            else:
                for x in range(len(self.clients)):
                    client = self.clients[x]
                    client[0].sendall(Encoder.encode_int(len(objects)))
                    for obj in objects:
                        for item in obj:
                            if isinstance(item, int):
                                client[0].sendall(Encoder.encode_int(item))
                            elif isinstance(item, str):
                                client[0].sendall(Encoder.encode_string(item))
                            else:
                                raise Exception("Invalid data type: ", str(type(item)))
                    client[0].sendall(Encoder.encode_int(int(lives[x])) + Encoder.encode_int(int(scores[x])))

                for x in range(len(self.clients)):
                    client = self.clients[x]
                    fl = Decoder.decode_int(client[0].recv(4))
                    self.engine.send_movement(x, fl & UP != 0, fl & DOWN != 0, fl & LEFT != 0, fl & RIGHT != 0, fl & SHOOT != 0)

            frame_end = datetime.datetime.now()
            delta = (frame_end - frame_start).microseconds
            if delta < self.frame_time:
                time.sleep((self.frame_time - delta) / 1000000)
            else:
                # Shit, we're running behind
                pass

    def close(self):
        for client in self.clients:
            client[0].close()






