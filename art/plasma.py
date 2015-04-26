from _baseclass import ArtBaseClass

from opc.nphue import h_to_rgb
import numpy as np


class Art(ArtBaseClass):

    description = "Classic plasma (almost)"

    def __init__(self, matrix, config):
        ones = np.ones(matrix.numpix).reshape((matrix.height, matrix.width))
        self.x = ones*np.arange(matrix.width)
        self.y = np.flipud(np.rot90(ones*np.arange(matrix.height)))

        self.base = 128000

    def start(self, matrix):
        pass

    def _dist(self, a, b, c, d):
        return np.sqrt((c-a)*(c-a)+(d-b)*(d-b))

    def refresh(self, matrix):

        xb = self.x + self.base
        yb = self.y + self.base

        c1 = self._dist(xb, self.y, 128.0, 128.0) / 8.0
        c2 = self._dist(self.y, self.y, 64.0, 64.0) / 8.0
        c3 = self._dist(self.x, yb / 7, 192.0, 64) / 7.0
        c4 = self._dist(self.y, self.x, 192.0, 100.0) / 8.0

        hue = np.sum(np.sin(c) for c in (c1, c2, c3, c4))
        hue = np.fmod(np.fabs(1+hue/2), 1.0)

        rgb = h_to_rgb(hue)

        for y in range(matrix.height):
            for x in range(matrix.width):
                matrix.drawPixel(x, y, rgb[x, y])

        self.base += 0.1

    def interval(self):
        return 60
