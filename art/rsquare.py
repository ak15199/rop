from math import sin, cos

from opc.colors import BLACK
from opc.hue import getColorGen

SCALE = 4


class Art(object):

    description = "Downsample a high-res image to improve perceived clarity"

    def __init__(self, matrix):
        self.hue = getColorGen(0.001)
        self.theta = 0.0

    def irnd(self, n):
        return int(round(n))

    def poly(self, matrix, reduction):
        tc = cos(self.theta)
        ts = sin(self.theta)

        r = self.r - reduction
        x = matrix.midWidth
        y = matrix.midHeight

        poly = [
            (self.irnd(x + r*tc - r*ts), self.irnd(y + r*tc + r*ts)),  # UL
            (self.irnd(x - r*tc - r*ts), self.irnd(y + r*tc - r*ts)),  # UR
            (self.irnd(x - r*tc + r*ts), self.irnd(y - r*tc - r*ts)),  # BR
            (self.irnd(x + r*tc + r*ts), self.irnd(y - r*tc + r*ts)),  # BL
            ]

        return poly

    def start(self, matrix):
        matrix.hq(True)

        # the width of the rectangle should allow for good fit when it is
        # rotated 45 degrees. We can invoke the work of pythagoras to determine
        # the hypotenuse, but rule of thumb (widest point is 1.7 broader than
        # the narrowest
        #
        self.r = min(matrix.midWidth, matrix.midHeight) * 0.7

    def refresh(self, matrix):
        self.theta += 0.05
        color = self.hue.next()

        matrix.clear()
        matrix.fillPoly(self.poly(matrix, 0), color)
        matrix.fillPoly(self.poly(matrix, 2*SCALE), BLACK)

    def interval(self):
        return 80
