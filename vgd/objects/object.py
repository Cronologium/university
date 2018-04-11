from objects.point import Point


class Object(object):
    def __init__(self, point, radius):
        self.point = point
        self.radius = radius
        self.died = False

    def move(self, xx, yy):
        self.point = self.point + Point(xx, yy)

    def set(self, xx, yy):
        self.point.x = xx
        self.point.y = yy

    def update(self):
        pass

    def intersects(self, other):
        if other.point - self.point < other.radius + self.radius:
            return True

    def hit(self):
        self.died = True

