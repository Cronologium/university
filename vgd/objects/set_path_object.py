import math
from copy import deepcopy

from objects.object import Object


class SetPathObject(Object):
    def __init__(self, points, rate, radius, cycles=False):
        self.points = points
        self.cycles = cycles
        if cycles:
            self.points.append(self.points[0])
        self.rate = rate
        self.last_point_touched = 0
        super().__init__(deepcopy(points[0]), radius)

    def move_on_line(self, point_to_reach, distance):
        if point_to_reach.x == self.point.x:
            if point_to_reach.y < self.point.y:
                self.move(0, -distance)
            else:
                self.move(0, distance)
            return
        elif point_to_reach.y == self.point.y:
            if point_to_reach.x < self.point.x:
                self.move(-distance, 0)
            else:
                self.move(distance, 0)
        else:
            m = (point_to_reach.y - self.point.y) / (point_to_reach.x - self.point.x)
            x_to_move = math.sqrt(distance ** 2 / (m ** 2 + 1))
            if point_to_reach.x < self.point.x:
                x_to_move *= -1
            y_to_move = x_to_move * m
            self.move(x_to_move, y_to_move)

    def update(self):
        dist = self.rate
        while dist > 0:
            if self.last_point_touched == len(self.points) - 1:
                if self.cycles:
                    self.last_point_touched = 0
                else:
                    return
            dist_left = self.points[self.last_point_touched + 1] - self.point
            if dist_left < dist:
                self.move_on_line(self.points[self.last_point_touched + 1], dist_left)
                dist -= dist_left
                self.last_point_touched += 1
            else:
                self.move_on_line(self.points[self.last_point_touched + 1], dist)
                dist = 0


