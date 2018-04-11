from layout.objects import GetEnemyShipReverseEight, GetEnemyShipEight
from objects.spawners.spawner import Spawner


class EnemyShipSpawner(Spawner):
    def __init__(self, cooldown, cooldown_left, reduce_factor):
        self.reversed = False
        super().__init__(cooldown, cooldown_left, reduce_factor)

    def spawn(self, center_point):
        obj = None
        if self.reversed:
            obj = GetEnemyShipReverseEight(center_point)
        else:
            obj = GetEnemyShipEight(center_point)
        self.reversed = not self.reversed
        return obj