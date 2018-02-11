from .baseclasses.barber import Barber

from random import random

from opc.hue import hsvToRgb


class Art(Barber):

    description = "Barber-pole-esque (dirty)"

    def _line(self, matrix, x1, x2, hue):
        for x in range(x1, x2):
            val = 0.8 + 0.2*random()
            matrix.drawPixel(x, 0, hsvToRgb(hue, 1, val))
