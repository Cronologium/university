from copy import deepcopy

from objects.asteroid import Asteroid
from objects.enemy_ship import EnemyShip
from objects.lazer import Lazer
from objects.player_ship import PlayerShip
from objects.point import Point
from objects.rock import Rock


class Engine:
    HEIGHT = 1080
    WIDTH = 800
    SPEED = 0.5
    CURRENT_SPEED = 0.5

    SECOND_POINTS = 1 / 60
    ROCK_POINTS = 2
    ASTEROID_POINTS = 10
    SHIP_POINTS = 200
    UFO_POINTS = 100

    def __init__(self, players=2):
        self.center = Point(Engine.WIDTH / 2, Engine.HEIGHT / 2)
        self.player_ships = [PlayerShip(x, Point(Engine.WIDTH / (players + 1) * (x + 1), PlayerShip.RADIUS * 1.5)) for x in range(players)]
        self.scores = [0 for _ in range(players)]
        self.friendly_objects = []
        self.enemy_objects = []
        Engine.CURRENT_SPEED = Engine.SPEED
        from objects.spawners.enemy_ship_spawner import EnemyShipSpawner
        from objects.spawners.ufo_spawner import UfoSpawner
        from objects.spawners.asteroid_spawner import AsteroidSpawner
        self.spawners = [
            AsteroidSpawner(75, 0, 0.02),
            UfoSpawner(90, 0, 0.02),
            EnemyShipSpawner(100, 0, 0.02)
        ]

    def update_object_set(self, object_set):
        new_objects = []
        for obj in object_set:
            result = obj.update()
            if result:
                new_objects.append(result)
        object_set += new_objects

    def check_score_change(self, friendly, enemy):
        if isinstance(friendly, PlayerShip):
            return
        elif isinstance(friendly, Lazer):
            if isinstance(enemy, Asteroid):
                self.scores[friendly.player_id] += Engine.ASTEROID_POINTS
            elif isinstance(enemy, Rock):
                self.scores[friendly.player_id] += Engine.ROCK_POINTS
            elif isinstance(enemy, EnemyShip):
                if enemy.autofire_rate is None:
                    self.scores[friendly.player_id] += Engine.UFO_POINTS
                else:
                    self.scores[friendly.player_id] += Engine.SHIP_POINTS

    def send_movement(self, pos, up, down, left, right, shoot):
        if self.player_ships[pos].died:
            return
        else:
            if up and down:
                up = down = False
            if left and right:
                left = right = False
            x_mul = 1 if up else -1 if down else 0
            y_mul = 1 if right else -1 if left else 0
            self.player_ships[pos].move_in_direction(x_mul, y_mul)
            if shoot:
                obj = self.player_ships[pos].fire()
                if obj:
                    self.friendly_objects.append(obj)

    def update(self):
        Engine.CURRENT_SPEED = ((self.center.y // Engine.HEIGHT) + 1) * Engine.SPEED
        self.center = self.center + Point(0, Engine.CURRENT_SPEED)

        self.update_object_set(self.friendly_objects)
        self.update_object_set(self.enemy_objects)

        for ship in self.player_ships:
            ship.update()
            ship.point.x = max(self.center.x - Engine.WIDTH / 2, min(ship.point.x, self.center.x + Engine.WIDTH / 2))
            ship.point.y = max(self.center.y - Engine.HEIGHT / 2, min(ship.point.y, self.center.y + Engine.HEIGHT / 2))

        for enemy in self.enemy_objects:
            if enemy.point.y < self.center.y - Engine.HEIGHT:
                enemy.hit()
            if isinstance(enemy, Lazer) and enemy.point.y > self.center.y + Engine.HEIGHT / 2 + enemy.radius:
                enemy.hit()

        for friendly in self.friendly_objects:
            if isinstance(friendly, Lazer) and friendly.point.y > self.center.y + Engine.HEIGHT / 2 + friendly.radius:
                friendly.hit()

        for friendly in self.friendly_objects + self.player_ships:
            for enemy in self.enemy_objects:
                if friendly.died:
                    break
                if enemy.died:
                    continue
                if friendly.intersects(enemy):
                    if isinstance(friendly, PlayerShip) and friendly.invulnerability_frames_left > 0:
                        continue
                    if isinstance(friendly, Lazer) and isinstance(enemy, Lazer):
                        continue
                    self.check_score_change(friendly, enemy)
                    friendly.hit()
                    result = enemy.hit()
                    if result:
                        if isinstance(result, list):
                            self.enemy_objects += result
                        else:
                            self.enemy_objects.append(result)

        self.friendly_objects = [friendly for friendly in self.friendly_objects if not friendly.died]
        self.enemy_objects = [enemy for enemy in self.enemy_objects if not enemy.died]


        lives = []
        scores = []
        all_ded = True

        for x in range(len(self.player_ships)):
            if not self.player_ships[x].died:
                self.scores[x] += Engine.SECOND_POINTS
                all_ded = False
            lives.append(self.player_ships[x].lives)
            scores.append(self.scores[x])


        if all_ded:
            print (all_ded, lives, scores)
            return [], [], []

        for spawner in self.spawners:
            result = spawner.update(deepcopy(self.center))
            if result:
                if isinstance(result, list):
                    self.enemy_objects += result
                else:
                    self.enemy_objects.append(result)

        object_list = []
        for entity in self.player_ships + self.friendly_objects + self.enemy_objects:
            obj = [int(entity.point.x - entity.radius / 2 - (self.center.x - Engine.WIDTH / 2)), Engine.HEIGHT - int(entity.point.y + entity.radius / 2 - (self.center.y - Engine.HEIGHT / 2))]
            if isinstance(entity, PlayerShip):
                if entity.died:
                    obj.append('')
                elif entity.invulnerability_frames_left > 0 and (entity.invulnerability_frames_left // 3) % 2 == 0:
                    obj.append('')
                else:
                    obj.append('ship')
            elif isinstance(entity, Lazer):
                if entity.friendly:
                    obj.append('redlazer')
                else:
                    obj.append('greenlazer')
            elif isinstance(entity, Asteroid):
                obj.append('bigasteroid')
            elif isinstance(entity, Rock):
                obj.append('smallasteroid')
            elif isinstance(entity, EnemyShip):
                if entity.autofire_rate is None:
                    obj.append('ufo')
                else:
                    obj.append('enemyship')
            else:
                print (str(type(entity)))
                obj.append('')
            object_list.append(obj)
        return object_list, lives, scores







