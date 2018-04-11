import random
from copy import deepcopy

from objects.asteroid import Asteroid
from objects.enemy_ship import EnemyShip
from objects.point import Point
from objects.set_path_object import SetPathObject
from server.engine import Engine

eight = [
    Point(-Engine.WIDTH / 2 + 100, Engine.HEIGHT - 100),
    Point(Engine.WIDTH / 2 - 100, Engine.HEIGHT + 100),
    Point(Engine.WIDTH / 2 - 100, Engine.HEIGHT - 100),
    Point(-Engine.WIDTH / 2 + 100, Engine.HEIGHT + 100)
]

reverse_eight = eight[::-1]

vertical_asteroid = Asteroid([Point(0, Engine.HEIGHT), Point(0, -Engine.HEIGHT)])
diagonal_asteroid = Asteroid([Point(0, Engine.HEIGHT), Point(0, -Engine.HEIGHT)])
ufo_horizontal = EnemyShip([Point(-Engine.WIDTH / 2 + 100, Engine.HEIGHT), Point(Engine.WIDTH / 2 - 100, Engine.HEIGHT)])
enemy_ship_eight = EnemyShip(eight, autofire_rate=60)
enemy_ship_reversed_eight = EnemyShip(reverse_eight, autofire_rate=60)

def get_translated_copy(point, obj):
    copy_obj = deepcopy(obj)
    if isinstance(copy_obj, SetPathObject):
        for x in range(len(copy_obj.points)):
            copy_obj.points[x] = obj.points[x] + point
        copy_obj.set(copy_obj.points[0].x, copy_obj.points[0].y)
    return copy_obj

def GetVerticalAsteroid(point, position):
    point.x += position
    return get_translated_copy(point, vertical_asteroid)

def GetHorizontalUfo(point):
    obj = get_translated_copy(point, ufo_horizontal)
    obj.set(random.randint(-Engine.WIDTH, Engine.WIDTH), obj.points[0].y)
    return obj

def GetEnemyShipEight(point):
    return get_translated_copy(point, enemy_ship_eight)

def GetEnemyShipReverseEight(point):
    return get_translated_copy(point, enemy_ship_reversed_eight)

def GetDiagonalAsteroid(point):
    inverted = random.randint(0, 1)
    if inverted == 0:
        inverted = -1
    point.x += inverted * Engine.WIDTH / 2
    obj = get_translated_copy(point, diagonal_asteroid)
    obj.points[1].x = random.randint(-Engine.WIDTH, Engine.WIDTH)
    return obj