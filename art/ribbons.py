from ._baseclass import ArtBaseClass

from math import sin, pi
from random import random

from opc.colors import RED, GREEN, BLUE
from opc.matrix import OPCMatrix, HQ


class Phase(object):

    def __init__(self, matrix, direction, color):
        self.matrix = OPCMatrix(matrix.width, matrix.height, None)
        self.color = (color)
        self.angle = random()*pi
        self.freq = (random()+0.5)*0.06
        self.direction = direction
        self.y = 0 if direction == "up" else self.matrix.height-1
        #self.x = self.matrix.width/2 if direction == "left" else self.matrix.width/2+1

    def clock(self, matrix):
        self.matrix.fade(0.96)
        self.matrix.scroll(self.direction)
        x = self.matrix.midWidth + self.matrix.midWidth*sin(self.angle)
        w = self.matrix.width/8
        self.matrix.drawLine(x-w, self.y, x+w, self.y, self.color)
        self.angle += self.freq
        matrix.add(self.matrix)


class Art(ArtBaseClass):

    description = "RGB variable frequency sine waves"

    def __init__(self, matrix, config):

        with HQ(matrix):
            self.phases = [Phase(matrix, direction, color)
                           for color in (RED, GREEN, BLUE)
                           for direction in ["up", "down"]]

    def start(self, matrix):
        matrix.hq()

    def refresh(self, matrix):
        matrix.clear()
        for phase in self.phases:
            phase.clock(matrix)

    def interval(self):
        return 150
