from math import sin, cos

from opc.colors import BLACK
from opc.hue import getHueGen
from opc.scaledmatrix import ScaledMatrix

SCALE = 4


class Art(object):

    description = "Downsample a high-res image to improve perceived clarity"

    def __init__(self, matrix):
        self.hue = getHueGen(0.001)
        self.theta = 0.0
        self.matrix = ScaledMatrix(matrix, scale=SCALE)

        # the width of the rectangle should allow for good fit when it is
        # rotated 45 degrees. We can invoke the work of pythagoras to determine
        # the hypotenuse, but rule of thumb (widest point is 1.7 broader than
        # the narrowest
        #
        self.r = min(self.matrix.midWidth, self.matrix.midHeight) * 0.7

    def irnd(self, n):
        return int(round(n))

    def poly(self, reduction):
        tc = cos(self.theta)
        ts = sin(self.theta)

        r = self.r - reduction
        x = self.matrix.midWidth
        y = self.matrix.midHeight

        poly = [
            (self.irnd(x + r*tc - r*ts), self.irnd(y + r*tc + r*ts)),  # UL
            (self.irnd(x - r*tc - r*ts), self.irnd(y + r*tc - r*ts)),  # UR
            (self.irnd(x - r*tc + r*ts), self.irnd(y - r*tc - r*ts)),  # BR
            (self.irnd(x + r*tc + r*ts), self.irnd(y - r*tc + r*ts)),  # BL
            ]

        return poly

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        self.matrix.clear()
        self.theta += 0.05
        color = self.hue.next()

        self.matrix.fillPoly(self.poly(0), color)
        self.matrix.fillPoly(self.poly(2*SCALE), BLACK)

        self.matrix.scaleDown()

    def interval(self):
        return 80
