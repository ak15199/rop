from opc.colors import *
from opc.hue import getHueGen
from opc.matrix import OPCMatrix

from math import sin, cos, pi

SCALE = 4

class Art:

    description = "Use a higher resolution image downsampled to improve perceived clarity"

    def __init__(self, matrix):
        self.hue = getHueGen(0.001)
        self.theta = 0.0
        self.matrix = OPCMatrix(SCALE*matrix.width, SCALE*matrix.height, None, True)
        self.x = SCALE * matrix.width / 2.0
        self.y = SCALE * matrix.height / 2.0
        self.r = 6.5 * SCALE

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
        self.theta += 0.05
        color = self.hue.next()
        self.matrix.shift(dv=0.8)

        for polys in range(0, SCALE*7, 2):
            self.matrix.drawPoly(self.poly(self.r-0.2*polys), color)

        matrix.copy(self.matrix)
  
    def interval(self):
        return 30

