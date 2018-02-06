from .pen import Pen
from math import sin, cos, pi, sqrt
from random import random


class Shrapnel(Pen):
    def __init__(self, matrix, motion_cycles, huedelta=0.001, saturation=1,
                 radius=0, decelerate=False):
        self.centerx = matrix.width/2.0
        self.centery = matrix.height/2.0
        self.cycles = motion_cycles
        self.decelerate = decelerate

        # we will reset some params to sensible values in a minute, so let's
        # not fuss with x, y, dx, dy now
        super(Shrapnel, self).__init__(
            matrix.width,
            matrix.height,
            0, 0, 0, 0,
            huedelta=huedelta,
            saturation=saturation,
            radius=radius
            )

        super(Shrapnel, self).setBumpStrategy(self._pause, x=True, y=True)

        self.reset(matrix)

    def _pause(self, x=None, y=None):
        self.paused = True

    def reset(self, matrix):
        # the furthest distance any pen will have to travel is on the diagonal
        w, h = matrix.width, matrix.height
        maxDimension = sqrt(w*w + h*h)

        # slowest pens need to cover the distance in cycles time, but there may
        # be some that go faster
        velocity = maxDimension/(2.0*self.cycles) + 0.05*random()*maxDimension

        angle = random()*2*pi
        self.dx = velocity * sin(angle)
        self.dy = velocity * cos(angle)

        self.x = self.centerx
        self.y = self.centery
        self.paused = False

    def clock(self, matrix):
        super(Shrapnel, self).clock(matrix)

        # optionally slow over time
        # XXX: this may cause problems for larger spans?
        if self.decelerate:
            self.dx *= 0.99
            self.dy *= 0.99

        return self.paused
