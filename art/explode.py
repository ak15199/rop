from opc.matrix import OPCMatrix
from utils.frange import frange
from utils.pen import Pen
from math import sin, cos, pi
from random import random

class Shrapnel(Pen):
    def __init__(self, matrix):
        self.centerx = matrix.width/2.0
        self.centery = matrix.height/2.0

        # we will reset some params to sensible values in a minute, so let's
        # not fuss with them now
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
        self.paused = False
        angle = random()*2*pi

        averageSize = (matrix.width+matrix.height)/2
        velocity = (averageSize/8+random()*4)/8

        velocityx = velocity * sin(angle)
        velocityy = velocity * cos(angle)

        self.x = self.centerx
        self.y = self.centery
        self.dx = velocityx
        self.dy = velocityy
        #print "set initial, x, y, dx, dy = ", initial, self.x, self.y, self.dx, self.dy

    def clock(self, matrix):
        super(Shrapnel, self).clock(matrix)
        self.dx *= 0.99
        self.dy *= 0.99
        return self.paused

class Art:

    PIECES = 32

    PAUSE_CYCLES = 10

    def __init__(self, matrix):
        self.pause = 0

        self.shrapnel=[]
        for i in range(self.PIECES):
            self.shrapnel.append( Shrapnel(matrix))

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)
        matrix.clear((80, 80, 90))

    def _update(self, matrix):
        done = 0
        for shrap in self.shrapnel:
            if shrap.clock(matrix):
                done += 1

        if done == self.PIECES:
            for shrap in self.shrapnel:
                shrap.reset(matrix)

            self.pause = self.PAUSE_CYCLES

    def refresh(self, matrix):
        matrix.shift(dv=0.8)
        if self.pause == 0:
            self._update(matrix)
        else:
            self.pause -= 1

    def interval(self):
        return 50

