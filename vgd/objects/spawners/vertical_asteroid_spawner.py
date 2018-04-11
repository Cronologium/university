import random

from layout.objects import GetVerticalAsteroid
from objects.spawners.spawner import Spawner
from server.engine import Engine


class VerticalAsteroidSpawner(Spawner):
    def __init__(self, cooldown, cooldown_left, reduce_factor):
        super().__init__(cooldown, cooldown_left, reduce_factor)

    def spawn(self, center_point):
        return GetVerticalAsteroid(center_point, random.randint(-Engine.WIDTH / 2, Engine.WIDTH / 2))