from opc.hue import hsvToRgb

from math import sqrt
from random import random

REPEATS = 4

class BarSet(object):

    def __init__(self, matrix, horizontal):
        # increments are split into primary and secondary. primary items(p)
        # increase on subsequent calls, secondary increments happen within
        # a call to draw a row.
        if horizontal:
            self.pdx, self.pdy = 0, 1
            self.sdx, self.sdy = 1, 0
        else:
            self.pdx, self.pdy = 1, 0
            self.sdx, self.sdy = 0, 1

        self.hue = random()

        cycleSize = int(sqrt(matrix.width*matrix.height)/REPEATS)
        self.bits = [ self._cointoss(0.3) for bit in range(cycleSize) ]

        self.px, self.py = 0, 0

    def _cointoss(self, chance):
        return random() < chance

    def draw(self, matrix):
        """
        draw a single row on the display. call many times in order to traverse the
        display. returns True when the far side of the display is reached.
        """

        sx, sy = 0, 0

        while sx < matrix.width and sy < matrix.height:
            for bit in self.bits:
                if bit:
                    matrix.drawPixel(sx + self.px, sy + self.py, hsvToRgb(self.hue, 1, 1))

                sx += self.sdx
                sy += self.sdy

        self.px += self.pdx
        self.py += self.pdy

        return self.px == matrix.width or self.py == matrix.height


class Art(object):

    description = "Generate checked plaid"

    def __init__(self, matrix):
        self.horizontal = True

    def start(self, matrix):
        matrix.clear()
        self.bar = BarSet(matrix, self.horizontal)

    def refresh(self, matrix):
        if self.bar.draw(matrix):
            self.horizontal = not self.horizontal
            self.bar = BarSet(matrix, self.horizontal)

    def interval(self):
        return 100
