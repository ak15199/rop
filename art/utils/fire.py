from opc.colors import BLACK
from opc.hue import getHueGen, hsvToRgb
from math import sqrt
from random import random, randint

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
        color = hsvToRgb(self.hue, 1, decay)
        matrix.drawPixel(self.x, self.y, color)

        self.x += self.dx
        if self.x == 0 or self.x >= (matrix.width-1):
            self.dx = -self.dx

        self.y += self.dy
        if self.y == 0 or self.y >= (matrix.height-1):
            self.dy = -self.dy

    def expired(self, matrix, expires):
        self.age += 1
        if self.age >= expires:
            matrix.drawPixel(self.x, self.y, BLACK)
            return True

        return False


class Gun(object):

    def __init__(self, matrix):
        self.points = []
        self.location = self._locationGenerator(matrix)
        self.hue = getHueGen(step=0.05, hue=random())

    def _locationGenerator(self, matrix):
        x, y = 0, 0

        while True:
            for x in range(matrix.width-1):
                yield {"x": x, "y": 0, "dx": -1, "dy": 1}
            for y in range(0, matrix.height-1):
                yield {"x": matrix.width-1, "y": y, "dx": -1, "dy": -1}
            for x in range(matrix.width-1, 0, -1):
                yield {"x": x, "y": matrix.height-1, "dx": 1, "dy": -1}
            for y in range(matrix.height-1, 0, -1):
                yield {"x": 0, "y": y, "dx": 1, "dy": 1}

    def fire(self, matrix):
        location = self.location.next()

        point = Point(location["x"], location["y"], location["dx"], location["dy"], self.hue.next())
        self.points.append(point)

        expires = int(matrix.numpix/2)
        self.points = [point for point in self.points if not point.expired(matrix, expires)]
        for point in self.points:
            point.update(matrix, expires)
