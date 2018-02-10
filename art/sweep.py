from ._baseclass import ArtBaseClass

from math import radians, sin
from random import random

from opc.colors import BLACK
from opc.hue import getColorGen, hsvToRgb
from opc.matrix import OPCMatrix


class Art(ArtBaseClass):

    description = "Barber-pole-esque (dirty)"

    def __init__(self, matrix, config):
        self.matrix = OPCMatrix(matrix.width, matrix.height, None)
        self.x = 5
        self.hue = 0
        self.ys = []

    def start(self, matrix):
        self.ys = [random() for y in range(matrix.height)]

    def refresh(self, matrix):
        self.matrix.clear()

        self.hue += 1.0/(6*4*matrix.width)

        
        for y, z in enumerate(self.ys):
            val = (1+sin(radians(360*z)))/2
            self.matrix.drawPixel(self.x, y, hsvToRgb(self.hue, 1, val))

        self.ys = [y+0.08*random() for y in self.ys]

        self.x = (self.x+1)%matrix.width

        self.matrix.maskbelow(55, BLACK)
        matrix.fade(0.99)
        matrix.add(self.matrix)

    def interval(self):
        return 120
