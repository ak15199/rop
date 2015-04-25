from _baseclass import ArtBaseClass

from math import sin, cos, pi
from random import random

from opc.colors import RED, GREEN, BLUE, BLACK
from opc.hue import getColorGen
from opc.matrix import OPCMatrix, HQ


class Phase(object):

    def __init__(self, matrix, direction, color):
        self.matrix = OPCMatrix(matrix.width, matrix.height, None)
        self.color = (color)
        self.angle = random()*pi
        self.freq = (random()+0.5)*0.06
        self.direction = direction
        self.x = 0 if direction == "left" else self.matrix.width-1

    def clock(self, matrix):
        self.matrix.fade(0.96)
        self.matrix.scroll(self.direction)
        y = self.matrix.midHeight + self.matrix.midHeight*sin(self.angle)
        h = self.matrix.height/8
        self.matrix.drawLine(self.x, y-h, self.x, y+h, self.color)
        self.angle += self.freq
        matrix.add(self.matrix)

class Art(ArtBaseClass):

    description = "RGB variable frequency sine waves"

    def __init__(self, matrix, config):
        with HQ(matrix):
            self.phases = [Phase(matrix, direction, color)
                    for color in (RED, GREEN, BLUE)
                    for direction in ["left", "right"]]

    def start(self, matrix):
        matrix.hq()

    def refresh(self, matrix):
        matrix.clear()
        for phase in self.phases:
            phase.clock(matrix)

    def interval(self):
        return 150
