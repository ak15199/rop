from opc.colors import BLACK
from opc.hue import getHueGen, hsvToRgb
from random import randint


class Point(object):

    def __init__(self, x, y, dx, dy, hue):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.hue = hue
        self.age = 0

    def update(self, matrix, expires):
        decay = 1-(float(self.age)/expires)
        self.age += 1
        color = hsvToRgb(self.hue, 1, decay)
        matrix.drawPixel(self.x, self.y, color)

        self.x += self.dx
        if self.x == 0 or self.x >= (matrix.width-1):
            self.dx = -self.dx

        self.y += self.dy
        if self.y == 0 or self.y >= (matrix.height-1):
            self.dy = -self.dy

    def expire(self, matrix):
        matrix.drawPixel(self.x, self.y, BLACK)


class Gun(object):

    def __init__(self, matrix):
        self.points = []
        self.expires = int(matrix.numpix/2)
        self.location = self._locationGenerator(matrix)
        self.hue = getHueGen(step=0.05, hue=randint(0, 100)/100.0)

    def _locationGenerator(self, matrix):
        x, y = 0, 0

        while True:
            for x in range(matrix.width-1):
                yield x, y, -1, 1

            for y in range(0, matrix.height-1):
                yield matrix.width-1,  y, -1, -1

            for x in range(matrix.width-1, 0, -1):
                yield x, matrix.height-1, 1, -1

            for y in range(matrix.height-1, 0, -1):
                yield 0, y, 1,  1

    def fire(self, matrix):
        x, y, dx, dy = next(self.location)

        point = Point(x, y, dx, dy, next(self.hue))
        self.points.append(point)

        if len(self.points) > self.expires:
            point = self.points.pop(0)
            point.expire(matrix)

        for point in self.points:
            point.update(matrix, self.expires)
