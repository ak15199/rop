from ._baseclass import ArtBaseClass

from random import random

from opc.hue import getColorGen, hsvToRgb


class Art(ArtBaseClass):

    description = "Barber-pole-esque (clean)"

    def __init__(self, matrix, config):
        self.width = matrix.width/4
        self.color = getColorGen(step=0.01)
        self.hue = 0

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        matrix.scroll("up")
        matrix.scroll("right")

        matrix.drawLine(0, 0, self.width, 0, next(self.color))

    def interval(self):
        return 120
