from random import random

from opc.colormap import Colormap
from opc.hue import hsvToRgb, getHueGen
from opc.matrix import OPCMatrix

from basecls.diamondsquare import DiamondSquare

class Art(object):

    description = "Terrain traversal (experimental)"

    def __init__(self, matrix):
        self.diamond = DiamondSquare(matrix.width*16, matrix.height, (matrix.width+matrix.height)/4)
        self.matrix = OPCMatrix(matrix.width*16, matrix.height, None, zigzag=matrix.zigzag)
        self.colormap = Colormap(100)

        self.colormap.gradient( 0, 45, (0, 0, 200), (40, 40, 255))
        self.colormap.gradient(45, 50, (40, 40, 255), (240, 240, 10))
        self.colormap.gradient(50, 60, (80, 60, 40), (0, 255, 0))
        self.colormap.gradient(60, 80, (0, 255, 0), (0, 200, 0))
        self.colormap.gradient(80, 95, (0, 200, 0), (120, 120, 120))
        self.colormap.gradient(95, 100, (120, 120, 120), (255, 255, 255))

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)
        self.x = 0
        self.diamond.generate(self.matrix, colormap=self.colormap)

    def refresh(self, matrix):
        matrix.copy(self.matrix, self.x, 0)
        self.x += 1

    def interval(self):
        return 60
