__author__ = 'rafe'

import random

import numpy


class Art(object):

    description = "Conway's Game of Life"

    def __init__(self, matrix, config):
        pass

    def start(self, matrix):
        init = [random.randint(0, 1) for _ in range(matrix.width * matrix.height)]
        self.lifes = numpy.array(init).reshape([matrix.width, matrix.height])
        self.prior = numpy.copy(self.lifes)
        for y in range(matrix.height):
            for x in range(matrix.width):
                self.lifes[x, y] = random.randint(0, 1)
        self.reset_count = 0
        self.global_countdown = 1000
        self.fade_countdown = 5

    def refresh(self, matrix):
        matrix.fade(0.9)

        if self.fade_countdown:
            self.fade_countdown -= 1
            return

        self.fade_countdown = 5

        width = matrix.width
        height = matrix.height

        lifes = self.lifes
        next = numpy.copy(lifes)
        for y in range(matrix.height):
            for x in range(matrix.width):
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
                        color = [255, 255, 0]
                    elif neighbors == 3:
                        color = [255, 0, 0]
                    else:
                        next[x, y] = 0
                        color = None
                else:
                    if neighbors == 3:
                        next[x, y] = 1
                        color = [0, 255, 0]
                    else:
                        next[x, y] = 0
                        color = None

                if color:
                    matrix.drawPixel(x, y, color)

        if (next == self.prior).all() or (next == self.lifes).all():
            self.reset_count += 1
        else:
            self.reset_count = 0

        self.prior = lifes
        self.lifes = next

        self.global_countdown -= 1

        if self.reset_count == 20 or not self.global_countdown:
            self.start(matrix)


    def interval(self):
        return 75