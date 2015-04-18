from math import sin, cos, pi
from random import random

from opc.colors import RED, GREEN, BLUE, GRAY50, BLACK
from opc.hue import getColorGen
from opc.matrix import OPCMatrix, HQ


class Phase(object):

    def __init__(self, matrix, color):
        self.matrix = OPCMatrix(matrix.width, matrix.height, None)
        self.color = color
        self.angle = random()*pi
        self.freq = (random()+0.5)*0.6

    def clock(self, matrix):
        w = self.matrix.width
        h = self.matrix.height

        self.matrix.clear(self.color)
        for x in range(0, w, w/4):
            self.matrix.fillRect(x, 0, w/8, h, BLACK)
        for y in range(0, h, h/4):
            self.matrix.fillRect(0, y, w, h/8, BLACK)

        self.matrix.rotate(self.angle)
        self.angle += self.freq

        matrix.add(self.matrix)

class Art(object):

    description = "RGB overlapping grids"

    def __init__(self, matrix):
        with HQ(matrix):
            self.phases = [Phase(matrix, color)
                    for color in (RED, GREEN, BLUE, GRAY50)]

    def start(self, matrix):
        matrix.hq()

    def refresh(self, matrix):
        matrix.clear()
        for phase in self.phases:
            phase.clock(matrix)

    def interval(self):
        return 100
