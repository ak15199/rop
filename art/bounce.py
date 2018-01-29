from opc.hue import getColorGen
from math import sqrt
from random import random


class Point(object):

    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def clock(self, matrix):
        self.x += self.dx
        if self.x <= 0 or self.x >= (matrix.width-1):
            self.dx = -self.dx

        self.y += self.dy
        if self.y <= 0 or self.y >= (matrix.height-1):
            self.dy = -self.dy

        return self


class Vector(object):

    def __init__(self, bases, color):
        self.points = [Point(base.x, base.y, base.dx, base.dy)
                       for base in bases]
        self.color = color

    def clock(self, matrix):
        for point in self.points:
            point.clock(matrix)

        p = self.points
        matrix.drawLine(p[0].x, p[0].y, p[1].x, p[1].y, self.color)


class Vectors(object):

    DELTA = 0.41

    def __init__(self, matrix, count):

        pointgen = self.positionGenerator(matrix)
        huegen = getColorGen(step=0.15, hue=random())
        self.vecs = [Vector(pointgen.next(), huegen.next())
                     for v in range(count)]

    def positionGenerator(self, matrix):
        x = matrix.width/3
        y = matrix.height/3

        points = [
            Point(x, matrix.midHeight, -self.DELTA, self.DELTA),
            Point(matrix.midWidth, y, self.DELTA, -self.DELTA)
            ]

        while True:
            yield points
            for point in points:
                point.clock(matrix)

    def clock(self, matrix):
        for vector in self.vecs:
            vector.clock(matrix)


class Art(object):

    description = "Bounce ends of a vector around the display"

    def __init__(self, matrix, config):
        vectorcount = int(matrix.smallest/4)
        self.vectors = Vectors(matrix, vectorcount)

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)
        matrix.clear()

    def refresh(self, matrix):
        matrix.shift(dh=0.98, dv=0.95)
        self.vectors.clock(matrix)
        matrix.rotate(-1)

    def interval(self):
        return 60
