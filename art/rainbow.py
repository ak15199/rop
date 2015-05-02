from _baseclass import ArtBaseClass

from math import sqrt

from opc.hue import hsvToRgb


class Art(ArtBaseClass):

    description = "Slow transition of hues across the display"

    def __init__(self, matrix, config):
        self.base = 0

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        self.base += 4
        h = matrix.height - 1

        for x in range(matrix.width):
            hue = (self.base+32*x) / (sqrt(matrix.numpix) * 64.0)
            for y in range(matrix.height):
                sat = min(1, 0.25 + (1.5*y)/h)
                val = min(1, 0.25 + (1.5*(h-y)/h))
                matrix.drawPixel(x, y, hsvToRgb(hue, sat, val))

    def interval(self):
        return 100
