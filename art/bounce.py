from opc.hue import hsvToRgb

from random import random
from math import fabs


class Art(object):

    description = "Bouncy ball"

    def __init__(self, matrix):
        self.radius = 1.5
        self.x = self.radius
        self.dx = 5
        self.timeslice = 50  # ms
        self.scale = 0.1
        self.dt = 100/self.timeslice*self.scale
        self.accel = 9.8
        self._reset(matrix)

    def start(self, matrix):
        matrix.clear()

    def _reset(self, matrix):
        self.color = random()
        self.y = matrix.height - 1 - self.radius
        self.dy = -1.3

    def refresh(self, matrix):
        matrix.shift(ds=0.75, dv=0.9)

        self.x = self.x + self.dx*self.dt
        self.y = self.y + self.dy*self.dt

        absdx, absdy = fabs(self.dx), fabs(self.dy)

        if self.x < self.radius:
            self.dx = absdx
        elif self.x >= (matrix.width-self.radius-1):
            self.dx = -absdx

        if self.y < self.radius:
            self.dy = absdy
        elif self.dy < 0.2 and self.dy > 0:
            self.dy = -absdy

        self.dy = self.dy - self.accel*self.dt

        if self.dy < 0 and self.y < self.radius:
            self._reset(matrix)
        else:
            matrix.fillCircle(self.x, self.y, self.radius,
                              hsvToRgb(self.color))

    def interval(self):
        return self.timeslice
