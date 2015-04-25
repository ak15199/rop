from _baseclass import ArtBaseClass

from math import sin, cos, sqrt
from random import random

from opc.colors import BLACK
from opc.hue import getColorGen

SCALE = 4


class Art(ArtBaseClass):

    description = "Demo image rotation"

    def __init__(self, matrix, config):
        self.hue = getColorGen(0.006)
        self.margin = sqrt(matrix.numpix) * 0.7
        self.direction = 5

    def start(self, matrix):
        matrix.hq(True)

    def refresh(self, matrix):
        color = self.hue.next()
        matrix.fillPoly([
            (matrix.width/2, self.margin),
            (self.margin, matrix.height-self.margin),
            (matrix.width-self.margin, matrix.height-self.margin),
            ], color
            )

        if random()<0.1:
            self.direction = -self.direction
        matrix.rotate(self.direction)

    def interval(self):
        return 80
