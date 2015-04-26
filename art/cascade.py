from _baseclass import ArtBaseClass
import numpy as np

from opc.colors import BLACK
from opc.hue import hsvToRgb

from math import fmod, sin, cos


class ClearTrain(object):
    def __init__(self, length):
        self.length = length
        self.points = [(0, 0) for i in range(length)]
        self.head = 0

    def add(self, matrix, x, y):
        x0, y0 = self.points[self.head]

        matrix.drawPixel(x0, y0, BLACK)
        self.points[self.head] = (x, y)

        self.head = (self.head + 1) % self.length


DELTA_AMP = 0.09
DELTA_ANG = 0.033
DELTA_HUE = 0.006
TRAIN_LEN = 16

TUNE_ME = 1.03


class Art(ArtBaseClass):

    description = "Color cascade (needs tuning for > 32x32)"

    def __init__(self, matrix, config):
        self.hue = 0
        self.ang = 0
        self.amp = 0
        self.train = ClearTrain(TRAIN_LEN)

    def start(self, matrix):
        matrix.clear()

    def refresh(self, matrix):
        # this relies on the fact that the pixels we seed get multiplied and
        # overfow the uint8
        matrix.blur(3)
        matrix.buf.buf = (TUNE_ME*matrix.buf.buf).astype(np.uint8)

        self.amp += DELTA_AMP
        if self.amp >= 1 and False:
            self.amp = 0

        self.hue += DELTA_HUE

        self.ang += DELTA_ANG

        xcenter = matrix.width / 2.0
        ycenter = matrix.height / 2.0
        amp = sin(self.amp)

        tx = amp * sin(self.ang)
        ty = amp * cos(self.ang)

        x = xcenter + xcenter * tx
        y = ycenter + ycenter * ty
        color = hsvToRgb(fmod(self.hue, 1), 1, 1)
        matrix.drawPixel(x, y, color)
        self.train.add(matrix, x, y)

    def interval(self):
        return 40
