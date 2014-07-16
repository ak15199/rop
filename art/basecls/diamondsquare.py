from opc.matrix import OPCMatrix
from opc.hue import hsvToRgb

from random import random

from art.utils.array import array

class DiamondSquare(object):

    """
    ported from http://www.bluh.org/code-the-diamond-square-algorithm/
    """
    def __init__(self, width, height, featureSize=None):
        self.width = width
        self.height = height
        if featureSize is None:
            self.featureSize = (self.width+self.height)/4
        else:
            self.featureSize = featureSize

        self.values = array([self.width, self.height], 0.0)

    def _getSample(self, x, y):
        return self.values[x % self.width][y % self.height]

    def _setSample(self, x, y, value):
        self.values[x % self.width][y % self.height] = value

    def _sampleSquare(self, x, y, size, value):
        hs = size / 2

        a = self._getSample(x - hs, y - hs)
        b = self._getSample(x + hs, y - hs)
        c = self._getSample(x - hs, y + hs)
        d = self._getSample(x + hs, y + hs)

        self._setSample(x, y, ((a + b + c + d) / 4.0) + value)

    def _sampleDiamond(self, x, y, size, value):
        hs = size / 2

        a = self._getSample(x - hs, y)
        b = self._getSample(x + hs, y)
        c = self._getSample(x, y - hs)
        d = self._getSample(x, y + hs)

        self._setSample(x, y, ((a + b + c + d) / 4.0) + value)

    def _rand(self):
         return 2*random() - 1

    def _diamondSquare(self, stepsize, scale):
        halfstep = stepsize / 2

        for y in range(0, self.height+halfstep, stepsize):
            for x in range(0, self.width+halfstep, stepsize):
                self._sampleSquare(halfstep+x, halfstep+y, stepsize, self._rand() * scale)

        for y in range(0, self.height, stepsize):
            for x in range(0, self.width, stepsize):
                self._sampleDiamond(x + halfstep, y, stepsize, self._rand() * scale)
                self._sampleDiamond(x, y + halfstep, stepsize, self._rand() * scale)

    def _generate(self):
        samplesize = self.featureSize
        scale = 1.0

        # seed initial values
        for y in range(0, self.height, samplesize):
            for x in range(0, self.width, samplesize):
                self._setSample(x, y, self._rand())

        # iterate through the intermediate spaces
        while samplesize > 1:
            self._diamondSquare(samplesize, scale)
            samplesize /= 2
            scale /= 2.0

    def _translate(self, matrix, hue, colormap):
        vmin =  100.0
        vmax = -100.0

        for x in range(self.width):
            for y in range(self.height):
                value = self.values[x][y]
                vmin = min(value, vmin)
                vmax = max(value, vmax)

        vscale = 1.0/(vmax-vmin)

        for x in range(self.width):
            for y in range(self.height):
                value = vscale * (self.values[x][y] - vmin)
                if hue is not None:
                    color = hsvToRgb(hue+value/5, 1, value)
                else:
                    color = colormap.convert(value, 1)

                matrix.drawPixel(x, y, color)

    def generate(self, matrix, hue=None, colormap=None):
        self._generate()
        self._translate(matrix, hue, colormap)
