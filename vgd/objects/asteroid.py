from copy import deepcopy

from objects.rock import Rock
from objects.set_path_object import SetPathObject


class Asteroid(SetPathObject):
    RATE = 2
    RADIUS = 50

    def __init__(self, points):
        super().__init__([deepcopy(point) for point in points], Asteroid.RATE, Asteroid.RADIUS)

    def hit(self):
        super().hit()
        return [
            Rock(self.point, -0.894, -1.195),
            Rock(self.point, 0, -2),
            Rock(self.point, 0.894, -1.195)
        ]