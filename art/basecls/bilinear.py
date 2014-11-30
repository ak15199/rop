from math import fmod
from random import random

from opc.hue import hsvToRgb


class Bilinear(object):

    def __init__(self, matrix, bits=None):
        self.bits = bits
        self.cornerValueDeltas = [
            self._delta(), self._delta(), self._delta(), self._delta(),
            ]

        self.cornerValues = [
            .1, .2, .3, .4,
            ]

    def _delta(self):
        return 0.001 + random() * 0.007

    def start(self, matrix):
        matrix.clear()

    def _weightedAverage(self, v0, v1, percent):
        return v0 + (v1-v0)*percent

    def _bilinearInterp(self, gun, px, py):
        xi0 = self._weightedAverage(gun[0], gun[1], px)
        xi1 = self._weightedAverage(gun[2], gun[3], px)

        return self._weightedAverage(xi0, xi1, py)

    def _percent(self, v, max):
        return (v+1.0)/max

    def _interpolate(self, rgb, px, py):
        return tuple([self._bilinearInterp(gun, px, py) for gun in rgb])

    def _rotate(self, array):
        return zip(*array[::-1])

    def refresh(self, matrix):

        """
        For any pair of colors represented as a hue, we need to calculate
        the distance between those two hues for each of the rgb components
        of the color. For the set of four corners, we have to interpolate
        each gun independently.
        """
        rgbs = self._rotate([hsvToRgb(self.cornerValues[i]) for i in range(4)])

        for x in range(matrix.width):
            px = self._percent(x, matrix.width)
            for y in range(matrix.height):
                py = self._percent(y, matrix.height)
                rgb = self._interpolate(rgbs, px, py)
                matrix.drawPixel(x, y, rgb)

        for i in range(4):
            new = self.cornerValues[i] + self.cornerValueDeltas[i]
            self.cornerValues[i] = fmod(new, 1.0)

        if self.bits is not None:
            matrix.buf.downSample(self.bits)

    def interval(self):
        return 100
