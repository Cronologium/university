from objects.lazer import Lazer
from objects.set_path_object import SetPathObject


class EnemyShip(SetPathObject):
    RATE = 3
    RADIUS = 25

    def __init__(self, points, autofire_rate=None):
        self.autofire_rate = autofire_rate
        self.last_fired = 0
        rate = EnemyShip.RATE
        if self.autofire_rate is None:
            rate *= 1.5
        super().__init__(points, rate, EnemyShip.RADIUS, cycles=True)

    def update(self):
        super().update()
        if self.autofire_rate:
            if self.last_fired == self.autofire_rate:
                self.last_fired = 1
                return Lazer(self, False)
            self.last_fired += 1
