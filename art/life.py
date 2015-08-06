__author__ = 'rafe'

from opc.hue import hue

import math
import random
import numpy

HSCALE = 0.1
RESET_INTERVAL = 20


class Art(object):

    description = "Conway's Game of Life"

    def __init__(self, matrix, config):
        self._interval = 300 if math.sqrt(matrix.numpix) < 20 else 75
        self.hue = random.random()
        self._init(matrix)

    def start(self, matrix):
        pass

    def _init(self, matrix):
        self.lifes = numpy.empty([matrix.width, matrix.height])
        self.prior = numpy.copy(self.lifes)

        for y in range(matrix.height):
            for x in range(matrix.width):
                self.lifes[x, y] = bool(random.getrandbits(1))

        self.reset_counter = 0

    def _hue(self, offset):
        return hue(self.hue+HSCALE*offset)

    def _neighbors(self, x, y, width, height):
        minus_x = (x - 1) % width
        minus_y = (y - 1) % height
        plus_x = (x + 1) % width
        plus_y = (y + 1) % height
        lifes = self.lifes
        return [
                    lifes[minus_x, minus_y],
                    lifes[x, minus_y],
                    lifes[plus_x, minus_y],
                    lifes[minus_x, y],
                    lifes[plus_x, y],
                    lifes[minus_x, plus_y],
                    lifes[x, plus_y],
                    lifes[plus_x, plus_y],
                ].count(True)

    def refresh(self, matrix):
        self.hue += 0.01

        matrix.shift(dh=0.9, dv=0.8)

        width = matrix.width
        height = matrix.height

        lifes = self.lifes
        next = numpy.empty([width, height])
        pixelset = {_: [] for _ in range(4)}

        for y in range(height):
            for x in range(width):
                neighbors = self._neighbors(x, y, width, height)
                if lifes[x, y]:
                    if neighbors == 2 or neighbors == 3:
                        cell = neighbors
                    else:
                        cell = 0
                else:
                    cell = 1 if neighbors == 3 else 0

                if cell > 0:
                    pixelset[cell].append((x, y))
                    next[x, y] = True
                else:
                    next[x, y] = False

        for color, pixels in pixelset.iteritems():
            if len(pixels):
                matrix.drawPixels(pixels, self._hue(color))

        if (next == self.prior).all() or (next == self.lifes).all():
            self.reset_counter += 1
        else:
            self.reset_counter = 0

        self.prior = lifes
        self.lifes = next

        if self.reset_counter == RESET_INTERVAL:
            self._init(matrix)

    def interval(self):
        return self._interval
