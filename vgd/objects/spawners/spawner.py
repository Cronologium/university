class Spawner(object):
    def __init__(self, cooldown, cooldown_left, reduce_factor, min_cooldown=30):
        self.cooldown_left = cooldown_left
        self.cooldown = cooldown
        self.reduce_factor = reduce_factor
        self.min_cooldown = min_cooldown

    def spawn(self, center_point):
        return None

    def update(self, center_point):
        if self.cooldown_left < 0:
            self.cooldown_left = max(self.cooldown, self.min_cooldown) - 1
            self.cooldown -= self.cooldown * self.reduce_factor
            return self.spawn(center_point)
        else:
            self.cooldown_left -= 1