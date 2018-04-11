from objects.point import Point
from objects.set_path_object import SetPathObject


class Lazer(SetPathObject):
    RATE = 5
    RADIUS = 7

    def __init__(self, parent, friendly, rate=RATE, player_id=None):
        multiplier = 1 if friendly else -1
        self.friendly = friendly
        self.player_id = player_id
        if self.friendly:
            from server.engine import Engine
            super().__init__([Point(parent.point.x, parent.point.y), Point(parent.point.x, parent.point.y + 5000 * multiplier)], Engine.CURRENT_SPEED + rate, Lazer.RADIUS)
        else:
            super().__init__(
                [Point(parent.point.x, parent.point.y), Point(parent.point.x, parent.point.y + 5000 * multiplier)],
                rate, Lazer.RADIUS)
