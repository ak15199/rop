from ._baseclass import ArtBaseClass

from opc.hue import hsvToRgb

from random import random
from .utils.lfsr import compoundLfsr

HUEINCYCLES = 8


class Art(ArtBaseClass):

    description = "Use an LFSR to 'randomly' fill the display"

    def __init__(self, matrix, config):
        pass

    def start(self, matrix):
        # we could probably shuffle() up a range, but that sounds like
        # it'd be less of a challenge :)
        self.random = compoundLfsr(matrix.numpix)
        self.hue = random()
        matrix.clear()

    def refresh(self, matrix):
        try:
            pos = next(self.random)
        except:
            self.random = compoundLfsr(matrix.numpix)
            pos = next(self.random)

        # gently transition through all hues over HUEINCYCLES fills
        self.hue += 1.0/(matrix.numpix*HUEINCYCLES)
        color = hsvToRgb(self.hue, 1, 0.2+0.8*random())
        matrix.setStripPixel(pos, color)

    def interval(self):
        return 50
