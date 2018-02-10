from ._baseclass import ArtBaseClass

from random import random

from opc.hue import getColorGen, hsvToRgb


class Art(ArtBaseClass):

    description = "Barber-pole-esque (dirty)"

    def __init__(self, matrix, config):
        self.width = matrix.width/4
        self.hue = 0

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        matrix.scroll("up")
        matrix.scroll("right")

        self.hue += 0.01
        for x in range(0, 1+self.width):
            val = 0.8 + 0.2*random()
            matrix.drawPixel(x, 0, hsvToRgb(self.hue, 1, val))

    def interval(self):
        return 120
