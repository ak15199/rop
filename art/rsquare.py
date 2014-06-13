from opc.colors import *
from opc.hue import getHueGen
from opc.matrix import OPCMatrix

import dpyinfo
from math import sin, cos, pi

class Art:

    def __init__(self, matrix):
        self.hue = getHueGen(0.001)
        self.theta = 0.0
        self.scale = 4
        self.matrix = OPCMatrix(self.scale*dpyinfo.WIDTH, self.scale*dpyinfo.HEIGHT, None, True)
        self.x = self.scale * dpyinfo.WIDTH / 2
        self.y = self.scale * dpyinfo.HEIGHT / 2
        self.r = 6.5 * self.scale

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
        matrix.setFirmwareConfig(nointerp=True)

    def refresh(self, matrix):
        self.theta += 0.005
        color = self.hue.next()
        self.matrix.clear()
        for polys in range(self.scale*7):
            self.matrix.drawPoly(self.poly(self.r-0.2*polys), color)

        matrix.copy(self.matrix)
  
    def interval(self):
        return 30

