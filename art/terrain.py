from math import sin, cos
from random import random

from opc.colormap import Colormap
from opc.hue import hsvToRgb, getHueGen
from opc.matrix import OPCMatrix

from basecls.diamondsquare import DiamondSquare

SCALE=16

class Art(object):

    description = "Terrain traversal (experimental)"

    def __init__(self, matrix):
        self.width = matrix.width*SCALE
        self.height = matrix.height*SCALE

        self.diamond = DiamondSquare(self.width, self.height, (matrix.width+matrix.height)/4)
        self.matrix = OPCMatrix(self.width, self.height, None, zigzag=matrix.zigzag)
        self.colormap = Colormap(100)

        self.colormap.gradient( 0, 20, (0, 0, 150), (0, 0, 200))
        self.colormap.gradient(20, 45, (0, 0, 200), (40, 40, 255))
        self.colormap.gradient(45, 50, (40, 40, 255), (240, 240, 10))
        self.colormap.gradient(50, 60, (80, 60, 40), (0, 255, 0))
        self.colormap.gradient(60, 80, (0, 255, 0), (0, 200, 0))
        self.colormap.gradient(80, 95, (0, 200, 0), (120, 120, 120))
        self.colormap.gradient(95, 100, (120, 120, 120), (255, 255, 255))

        self.theta = 0
        self.radius = 0

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)
        self.diamond.generate(self.matrix, colormap=self.colormap)

    def refresh(self, matrix):
        self.theta += .01
        self.radius -= 0.05

        if self.radius<4:
            self.radius = (self.width+self.height)/4

        x = self.width/2 + self.radius * sin(self.theta)
        y = self.height/2 + self.radius * cos(self.theta)
        
        matrix.copy(self.matrix, x, y)

    def interval(self):
        return 60
