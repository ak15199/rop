from utils.pen import Pen
from math import sin, cos, pi, sqrt
from random import random


class Shrapnel(Pen):
    def __init__(self, matrix, motion_cycles):
        self.centerx = matrix.width/2.0
        self.centery = matrix.height/2.0
        self.cycles = motion_cycles

        # we will reset some params to sensible values in a minute, so let's
        # not fuss with x, y, dx, dy now
        super(Shrapnel, self).__init__(
            matrix.width,
            matrix.height,
            0, 0, 0, 0,
            )

        super(Shrapnel, self).setBumpStrategy(self._pause, x=True, y=True)

        self.reset(matrix)

    def _pause(self, x=None, y=None):
        self.paused = True

    def reset(self, matrix):
        # the furthest distance any pen will have to travel is on the diagonal
        maxDimension = sqrt(matrix.width*matrix.width + matrix.height*matrix.height)

        # slowest pens need to cover the distance in cycles time, but there may be
        # some that go faster
        velocity = maxDimension/(2.0*self.cycles) + 0.05*random()*maxDimension

        angle = random()*2*pi
        self.dx = velocity * sin(angle)
        self.dy = velocity * cos(angle)

        self.x = self.centerx
        self.y = self.centery
        self.paused = False

    def clock(self, matrix):
        super(Shrapnel, self).clock(matrix)

        # slow over time
        # XXX: this may cause problems for larger spans?
        self.dx *= 0.99
        self.dy *= 0.99
        return self.paused


class Art(object):

    description = "And then it exploded..."

    PAUSE_CYCLES = 10

    def __init__(self, matrix):
        self.pause = 0
        self.pieces = int(sqrt(matrix.numpix)/1.5)

        cycles = int(sqrt(matrix.numpix)*2)
        self.shrapnel = [Shrapnel(matrix, cycles) for i in range(self.pieces)]

    def start(self, matrix):
        matrix.clear()

    def _update(self, matrix):
        done = 0
        for shrap in self.shrapnel:
            if shrap.clock(matrix):
                done += 1

        if done == self.pieces:
            for shrap in self.shrapnel:
                shrap.reset(matrix)

            self.pause = self.PAUSE_CYCLES

    def refresh(self, matrix):
        matrix.shift(dv=0.7)
        if self.pause == 0:
            self._update(matrix)
        else:
            self.pause -= 1

    def interval(self):
        return 50
