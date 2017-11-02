class Matrix:
    def __init__(self, x, y):
        self.m = [[0 for _ in xrange(y)] for _ in xrange(x)]
        self.set_x = [0 for _ in xrange(x)]
        self.set_y = [0 for _ in xrange(y)]

    def get_row(self, x):
        r = self.m[x]
        return (self.set_x[x] == len(r), r)

    def get_column(self, y):
        c = [self.m[x][y] for x in xrange(len(self.m))]
        return self.set_y[y] == len(c), c

    def set(self, x, y, v):
        self.m[x][y] = v
        self.set_x[x] += 1
        self.set_y[y] += 1

    def __str__(self):
        return '\n'.join([' '. join([str(self.m[x][y]) for y in xrange(len(self.m[x]))]) for x in xrange(len(self.m))])
