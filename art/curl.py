from _baseclass import ArtBaseClass

from opc.hue import hsvToRgb

from math import fmod, sin, cos

DELTA_AMP = 0.09
DELTA_ANG = 0.033
DELTA_HUE = 0.006


class Art(ArtBaseClass):

    description = "Loop the loop"

    def __init__(self, matrix, config):
        self.hue = 0
        self.ang = 0
        self.amp = 0

    def start(self, matrix):
        matrix.hq()
        matrix.clear()

    def refresh(self, matrix):
        matrix.fade(0.98)

        self.amp += DELTA_AMP
        self.hue += DELTA_HUE
        self.ang += DELTA_ANG

        amp = sin(self.amp)

        tx = amp * sin(self.ang)
        ty = amp * cos(self.ang)

        x = matrix.midWidth + matrix.midWidth * tx
        y = matrix.midHeight + matrix.midHeight * ty

        color = hsvToRgb(fmod(self.hue, 1), 1, 1)

        matrix.drawRect(x-4, y-4, 8, 8, color)

    def interval(self):
        return 40
