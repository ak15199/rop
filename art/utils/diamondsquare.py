from opc.hue import hsvToRgb
from opc.nphue import h_to_rgb

import numpy as np

from random import random
import sys
try:
    from exceptions import AttributeError
except ModuleNotFoundError:
    pass

from art.utils.array import array
from opc.utils.prof import timefunc


class DiamondSquareAlgorithm(object):

    """
    ported from http://www.bluh.org/code-the-diamond-square-algorithm/
    """
    def __init__(self, width, height, featureSize=None):
        self.width = width
        self.height = height
        if featureSize is None:
            self.featureSize = int((self.width+self.height)/4)
        else:
            self.featureSize = int(featureSize)

        self.values = array([self.width, self.height], 0.0)

    def _getSample(self, x, y):
        return self.values[x % self.width][y % self.height]

    def _setSample(self, x, y, value):
        self.values[x % self.width][y % self.height] = value

    def _sampleSquare(self, x, y, size, value):
        hs = int(size / 2)

        a = self._getSample(x - hs, y - hs)
        b = self._getSample(x + hs, y - hs)
        c = self._getSample(x - hs, y + hs)
        d = self._getSample(x + hs, y + hs)

        self._setSample(x, y, ((a + b + c + d) / 4.0) + value)

    def _sampleDiamond(self, x, y, size, value):
        hs = int(size / 2)

        a = self._getSample(x - hs, y)
        b = self._getSample(x + hs, y)
        c = self._getSample(x, y - hs)
        d = self._getSample(x, y + hs)

        self._setSample(x, y, ((a + b + c + d) / 4.0) + value)

    def _rand(self):
        return 2*random() - 1

    def _diamondSquare(self, stepsize, scale):
        stepsize = int(stepsize)
        halfstep = int(stepsize/2)

        for y in range(0, self.height+halfstep, stepsize):
            for x in range(0, self.width+halfstep, stepsize):
                self._sampleSquare(halfstep+x, halfstep+y,
                                   stepsize, self._rand() * scale)

        for y in range(0, self.height, stepsize):
            for x in range(0, self.width, stepsize):
                self._sampleDiamond(x + halfstep, y, stepsize,
                                    self._rand() * scale)
                self._sampleDiamond(x, y + halfstep, stepsize,
                                    self._rand() * scale)

    def generate(self):
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

    @timefunc
    def translate(self, matrix, hue=None, colormap=None):
        if hue is None and colormap is None:
            raise AttributeError("Need either a hue or colormap")

        vmin = np.min(self.values)
        vmax = np.max(self.values)
        values = (self.values-vmin)/(vmax-vmin)

        if colormap is None:
            for x in range(self.width):
                for y in range(self.height):
                    color = hsvToRgb(hue+values[x, y]/5, 1, values[x, y])
                    matrix.drawPixel(x, y, color)
        else:
            buffer = colormap.apply(values)
            matrix.copyBuffer(buffer)
