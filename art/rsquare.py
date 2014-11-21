from math import sin, cos, pi, sqrt

from opc.colors import *
from opc.hue import getHueGen
from opc.scaledmatrix import ScaledMatrix


class Art(object):

    description = "Use a higher resolution image downsampled to improve perceived clarity"

    def __init__(self, matrix):
        self.hue = getHueGen(0.001)
        self.theta = 0.0
        self.matrix = ScaledMatrix(matrix)
        self.x = self.matrix.midWidth
        self.y = self.matrix.midHeight

        # the width of the rectangle should allow for good fit when it is
        # rotated 45 degrees. We can invoke the work of pythagoras to determine
        # the hypotenuse, but rule of thumb (widest point is 1.7 broader than
        # the narrowest
        #
        self.r = min(self.matrix.midWidth, self.matrix.midHeight) * 0.7

    def irnd(self, n):
        return int(round(n))

    def poly(self, r):
        tc = cos(self.theta)
        ts = sin(self.theta)

        poly = [
                (self.irnd(self.x + r * tc - r * ts) ,  self.irnd(self.y + r * tc  + r * ts)), # UL
                (self.irnd(self.x - r * tc - r * ts) ,  self.irnd(self.y + r * tc  - r * ts)), # UR
                (self.irnd(self.x - r * tc + r * ts) ,  self.irnd(self.y - r * tc  - r * ts)), # BR
                (self.irnd(self.x + r * tc + r * ts) ,  self.irnd(self.y - r * tc  + r * ts)), # BL
            ]

        return poly

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        self.matrix.clear()
        self.theta += 0.05
        color = self.hue.next()
        self.matrix.shift(dv=0.8)

        for polys in range(0, self.matrix.scale*7, 2):
            self.matrix.drawPoly(self.poly(self.r-0.2*polys), color)

        self.matrix.scaleDown()

    def interval(self):
        return 30

