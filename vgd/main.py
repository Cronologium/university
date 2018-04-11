import sys

from client.gameclient import GameClient
from communication.decoders import Decoder
from communication.encoders import Encoder
from server.gameserver import GameServer


def main(how, host='localhost', port=5005, players=1):
    if how == 'client':
        game_client = GameClient(host, int(port))
        game_client.connect()
        try:
            game_client.update()
        except KeyboardInterrupt:
            game_client.close()
    elif how == 'server':
        game_server = GameServer(host, int(port), fps=60)
        game_server.connect(players)
        try:
            game_server.update()
        except KeyboardInterrupt:
            game_server.close()
    elif how == 'test':
        print(Decoder.decode_int(Encoder.encode_int(5)))
        print(Encoder.encode_string('test'))
        bites = Encoder.encode_string('test')
        print(Decoder.decode_int(bites[:4]))
        print(Decoder.decode_string(bites[4:]))

if __name__ == '__main__':
    main(*sys.argv[1:])