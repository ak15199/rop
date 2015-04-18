from opc.colors import BLACK
from opc.hue import hsvToRgb

from random import random, randrange
from math import fmod

HUEDELTA = 0.0005


class Pen(object):
    def __init__(self, width, height, x, y, dx=1, dy=1, persist=True,
                 hue=None, saturation=1, huedelta=HUEDELTA, radius=0):

        self.hue = random() if hue is None else hue
        self.value = 1
        self.x, self.x0 = x, x
        self.y, self.y0 = y, y
        self.w = width
        self.h = height
        self.dx = dx
        self.dy = dy
        self.ax = self.trap
        self.ay = self.trap
        self.persist = persist
        self.huedelta = huedelta
        self.saturation = saturation
        self.radius = radius

    def setValue(self, value):
        self.value = value

    def trap(self, x=False, y=False):
        raise Exception("Bump strategy not set (%d, %d)" % (x, y))

    def setBumpStrategy(self, func, x=False, y=False):
        if x:
            self.ax = func
        if y:
            self.ay = func

    # Here are our bumpstrategies that can be reused. Simply put, you pick
    # one of these to execute when the pen reaches the limits of the display.
    # you can also set your own bump strategy by providing a method or
    # methods.
    def reset(self, x=False, y=False):
        if x:
            self.x = self.x0
        if y:
            self.y = self.y0

    def reverse(self, x=False, y=False):
        if x:
            self.dx = -self.dx
        if y:
            self.dy = -self.dy

    def random(self, x=False, y=False):
        if x:
            self.x = randrange(self.w)
        if y:
            self.y = randrange(self.h)

    def none(self, x=False, y=False):
        pass

    def clock(self, matrix):
        if not self.persist:
            matrix.drawPixel(self.x, self.y, BLACK)

        self.x += self.dx
        if (self.x < 1 and self.dx < 0) or \
                (self.x >= self.w-1 and self.dx > 0):
            self.ax(x=True)

        self.y += self.dy
        if (self.y < 1 and self.dy < 0) or \
                (self.y >= self.h-1 and self.dy > 0):
            self.ay(y=True)

        if self.radius == 0:
            matrix.drawPixel(self.x, self.y,
                             hsvToRgb(self.hue, s=self.saturation, v=self.value))
        else:
            matrix.fillCircle(self.x, self.y, self.radius,
                              hsvToRgb(self.hue, s=self.saturation, v=self.value))

        self.hue = fmod(self.hue + self.huedelta, 1)
