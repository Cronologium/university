from objects.object import Object


class Rock(Object):
    RADIUS = 20

    def __init__(self, point, x_dir, y_dir):
        self.direction_x = x_dir
        self.direction_y = y_dir
        super().__init__(point, Rock.RADIUS)

    def update(self):
        self.move(self.direction_x, self.direction_y)