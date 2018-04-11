import os
import socket
import time
from threading import Thread

import pygame

from communication.decoders import Decoder
from communication.encoders import Encoder
from communication.opcodes import *


class GameClient:
    ASSETS_ROOT = os.path.join('assets')
    LOGO_FILE = os.path.join(ASSETS_ROOT, 'life.png')

    def __init__(self, host, port):
        # load assets
        self.assets = {
            'ship': pygame.image.load(os.path.join(GameClient.ASSETS_ROOT, 'player.png')),
            'bigasteroid': pygame.image.load(os.path.join(GameClient.ASSETS_ROOT, 'meteorBig.png')),
            'smallasteroid': pygame.image.load(os.path.join(GameClient.ASSETS_ROOT, 'meteorSmall.png')),
            'ufo': pygame.image.load(os.path.join(GameClient.ASSETS_ROOT, 'enemyUFO.png')),
            'life': pygame.image.load(os.path.join(GameClient.ASSETS_ROOT, 'life.png')),
            'enemyship': pygame.image.load(os.path.join(GameClient.ASSETS_ROOT, 'enemyShip.png')),
            'redlazer': pygame.image.load(os.path.join(GameClient.ASSETS_ROOT, 'laserRed.png')),
            'greenlazer': pygame.image.load(os.path.join(GameClient.ASSETS_ROOT, 'laserGreen.png')),
        }
        self.host = host
        self.port = port
        self.server = None
        self.height = 0
        self.width = 0
        self.font = 0
        self.screen = None
        self.controller_thread = None
        self.flags = {
            'up': False,
            'down': False,
            'left': False,
            'right': False,
            'space': False
        }
        self.quit = False

    def connect(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.host, self.port))

        data_size = Decoder.decode_int(self.server.recv(4))
        resolution_string = Decoder.decode_string(self.server.recv(data_size))
        self.height, self.width = resolution_string.split('x')

        self.height = int(self.height)
        self.width = int(self.width)

        pygame.init()
        pygame.font.init()

        pygame.display.set_icon(self.assets['life'])
        pygame.display.set_caption("Rail Space Shooter")

        self.font = pygame.font.SysFont('Arial', 30)
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.assets['ship'] =  pygame.transform.scale(self.assets['ship'], (80, 80))
        self.assets['bigasteroid'] = pygame.transform.scale(self.assets['bigasteroid'], (100, 100))
        self.assets['smallasteroid'] = pygame.transform.scale(self.assets['smallasteroid'], (40, 40))

        self.assets['ufo'] = pygame.transform.scale(self.assets['ufo'], (50, 50))
        self.assets['enemyship'] = pygame.transform.scale(self.assets['enemyship'], (50, 50))

        self.controller_thread = Thread(target=self.control)
        self.controller_thread.start()

    def control(self):
        while not self.quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == UP_KEY:
                        self.flags['up'] = True
                    if event.key == DOWN_KEY:
                        self.flags['down'] = True
                    if event.key == RIGHT_KEY:
                        self.flags['right'] = True
                    if event.key == LEFT_KEY:
                        self.flags['left'] = True
                    if event.key == SPACE_KEY:
                        self.flags['space'] = True
                elif event.type == pygame.KEYUP:
                    if event.key == UP_KEY:
                        self.flags['up'] = False
                    if event.key == DOWN_KEY:
                        self.flags['down'] = False
                    if event.key == RIGHT_KEY:
                        self.flags['right'] = False
                    if event.key == LEFT_KEY:
                        self.flags['left'] = False
                    if event.key == SPACE_KEY:
                        self.flags['space'] = False
            time.sleep(0.01)
        self.controller_thread = None

    def update(self):
        while not self.quit:
            size = Decoder.decode_int(self.server.recv(4))
            items = []
            for _ in range(size):
                x = Decoder.decode_int(self.server.recv(4))
                y = Decoder.decode_int(self.server.recv(4))
                asset_str_size = Decoder.decode_int(self.server.recv(4))
                asset = Decoder.decode_string(self.server.recv(asset_str_size))
                items.append([x, y, asset])
            lives = Decoder.decode_int(self.server.recv(4))
            score = Decoder.decode_int(self.server.recv(4))

            self.screen.fill((0, 0, 0))
            for item in items:
                if item[2] in self.assets:
                    self.screen.blit(self.assets[item[2]], (item[0], item[1]))

            score_surface = self.font.render('Score: {0}'.format(score), False, (255, 255, 255))
            lives_surface = self.font.render('Lives: {0}'.format(lives), False, (255, 255, 255))
            self.screen.blit(score_surface, (0, 0))
            self.screen.blit(lives_surface, (0, self.height - 45))
            pygame.display.flip()

            flags = 0
            if self.flags['up']:
                flags |= UP
            if self.flags['down']:
                flags |= DOWN
            if self.flags['left']:
                flags |= LEFT
            if self.flags['right']:
                flags |= RIGHT
            if self.flags['space']:
                flags |= SHOOT

            self.server.sendall(Encoder.encode_int(flags))


    def close(self):
        if self.controller_thread:
            self.controller_thread.join(1)
        self.server.close()