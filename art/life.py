__author__ = 'rafe'

from opc.hue import hue

import random
import numpy

HSCALE = 0.1
RESET_INTERVAL = 20


class Art(object):

    description = "Conway's Game of Life"

    def __init__(self, matrix, config):
        self.iterations = config.get('ITERATIONS', 1000)
        self.hscale = config.get('HSCALE', HSCALE)
        self._interval = config.get('INTERVAL', 300)

    def start(self, matrix):
        self.lifes = numpy.empty([matrix.width, matrix.height])
        self.prior = numpy.copy(self.lifes)

        for y in range(matrix.height):
            for x in range(matrix.width):
                self.lifes[x, y] = random.randint(0, 1)

        self.reset_counter = 0
        self.global_countdown = self.iterations

        self.hue = random.random()

    def _hue(self, offset):
        return hue(self.hue+self.hscale*offset)

    def refresh(self, matrix):
        matrix.shift(dh=0.9, dv=0.8)

        width = matrix.width
        height = matrix.height

        lifes = self.lifes
        next = numpy.copy(lifes)
        for y in range(height):
            for x in range(width):
                minus_x = (x - 1) % width
                minus_y = (y - 1) % height
                plus_x = (x + 1) % width
                plus_y = (y + 1) % height
                neighbors = sum([
                    lifes[minus_x, minus_y],
                    lifes[x, minus_y],
                    lifes[plus_x, minus_y],
                    lifes[minus_x, y],
                    lifes[plus_x, y],
                    lifes[minus_x, plus_y],
                    lifes[x, plus_y],
                    lifes[plus_x, plus_y],
                ])

                if lifes[x, y]:
                    if neighbors == 2:
                        next[x, y] = 1
                        color = self._hue(0)
                    elif neighbors == 3:
                        color = self._hue(1)
                    else:
                        next[x, y] = 0
                        color = None
                else:
                    if neighbors == 3:
                        next[x, y] = 1
                        color = self._hue(2)
                    else:
                        next[x, y] = 0
                        color = None

                if color:
                    matrix.drawPixel(x, y, color)

        if (next == self.prior).all() or (next == self.lifes).all():
            self.reset_counter += 1
        else:
            self.reset_counter = 0

        self.prior = lifes
        self.lifes = next

        self.global_countdown -= 1

        if self.reset_counter == RESET_INTERVAL or not self.global_countdown:
            self.start(matrix)

    def interval(self):
        return self._interval
