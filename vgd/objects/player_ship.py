import math

from objects.lazer import Lazer
from objects.object import Object


class PlayerShip(Object):
    RADIUS = 40
    SPEED = 20
    DIAGONAL_SPEED = SPEED * math.sqrt(0.5)
    LIVES = 3
    INVULNERABILITY_FRAMES = 120
    COOLDOWN = 5

    def __init__(self, id, point):
        self.id = id
        self.lives = PlayerShip.LIVES
        self.invulnerability_frames_left = 0
        self.cooldown = 0
        super().__init__(point, PlayerShip.RADIUS)

    def move_in_direction(self, x_mul, y_mul):
        if abs(x_mul) + abs(y_mul) == 0:
            return
        elif abs(x_mul) + abs(y_mul) == 1:
            self.move(PlayerShip.SPEED * x_mul, PlayerShip.SPEED * y_mul)
        else:
            self.move(PlayerShip.DIAGONAL_SPEED * x_mul, PlayerShip.DIAGONAL_SPEED * y_mul)

    def update(self):
        if self.invulnerability_frames_left > 0:
            self.invulnerability_frames_left -= 1
        if self.cooldown > 0:
            self.cooldown -= 1

    def hit(self):
        self.lives -= 1
        if self.lives == 0:
            super().hit()
        else:
            self.invulnerability_frames_left = PlayerShip.INVULNERABILITY_FRAMES

    def fire(self):
        if self.cooldown == 0:
            self.cooldown = PlayerShip.COOLDOWN
            return Lazer(self, True, 20, self.id)
