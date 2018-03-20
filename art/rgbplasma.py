from ._baseclass import ArtBaseClass

from opc.matrix import HQ
from random import random
import numpy as np


class Channel(object):

    def __init__(self, matrix):
        ones = np.ones(matrix.numpix).reshape((matrix.height, matrix.width))
        self.x = ones*np.arange(matrix.width)
        self.y = np.flipud(np.rot90(np.rot90(ones)*np.arange(matrix.height)))

        self.base = random()*128000

    def _dist(self, a, b, c, d):
        return np.sqrt((c-a)*(c-a)+(d-b)*(d-b))

    def refresh(self):
        self.base += 0.7

        xb = self.x + self.base
        yb = self.y + self.base

        c1 = self._dist(xb, self.y, 128.0, 128.0) / 8.0
        c2 = self._dist(self.y, self.y, 64.0, 64.0) / 8.0
        c3 = self._dist(self.x, yb / 7, 192.0, 64) / 7.0
        c4 = self._dist(self.y, self.x, 192.0, 100.0) / 8.0

        channel = np.sum(np.sin(c) for c in (c1, c2, c3, c4))
        return 255*np.fmod(np.fabs(1+channel/2), 1.0)


class Art(ArtBaseClass):

    description = "Plasma by RGB channel"

    def __init__(self, matrix, config):
        with HQ(matrix):
            self.channels = [Channel(matrix) for channel in range(3)]

    def start(self, matrix):
        matrix.hq()

    def refresh(self, matrix):

        channels = [channel.refresh() for channel in self.channels]

        for y in range(matrix.height):
            for x in range(matrix.width):
                matrix.drawPixel(x, y, (
                    channels[0][y, x],
                    channels[1][y, x],
                    channels[2][y, x],
                    ))

    def interval(self):
        return 60
