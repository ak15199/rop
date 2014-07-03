from opc.matrix import OPCMatrix
from random import random
from opc.hue import hsvToRgb, getHueGen

class Art:

    """
    ported from http://www.bluh.org/code-the-diamond-square-algorithm/
    """
    def __init__(self, matrix):
        self.width = matrix.width
        self.height = matrix.height
        self.hue = random()

        self.values = [ [None for y in range(self.height)] for x in range(self.width)]

    def start(self, matrix):
        pass

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

    def _seed(self, featureSize):
        for y in range(0, self.height, featureSize):
            for x in range(0, self.width, featureSize):
                self._setSample(x, y, self._rand())

    def _generate(self, featureSize):
        samplesize = featureSize
        scale = 1.0

        while samplesize > 1:
            self._diamondSquare(samplesize, scale)
            samplesize /= 2
            scale /= 2.0

    def refresh(self, matrix):
        featureSize = (matrix.width+matrix.height)/4
        self._seed(featureSize)
        self._generate(featureSize)

        vmin =  100.0
        vmax = -100.0

        for x in range(self.width):
            for y in range(self.height):
                value = self.values[x][y]
                vmin = min(value, vmin)
                vmax = max(value, vmax)

        vscale = 1.0/(vmax-vmin)
        self.hue += 0.01

        for x in range(self.width):
            for y in range(self.height):
                value = vscale * (self.values[x][y] - vmin)
                color = hsvToRgb(self.hue+value/5, 1, value)
                matrix.drawPixel(x, y, color)

    def interval(self):
        return 400
