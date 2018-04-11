from layout.objects import GetHorizontalUfo
from objects.spawners.spawner import Spawner


class UfoSpawner(Spawner):
    def __init__(self, cooldown, cooldown_left, reduce_factor):
        super().__init__(cooldown, cooldown_left, reduce_factor)

    def spawn(self, center_point):
        return GetHorizontalUfo(center_point)