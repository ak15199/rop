from random import random

from opc.colormap import Colormap
from opc.colors import *
from opc.hue import hsvToRgb, getHueGen
from opc.matrix import OPCMatrix

from art.utils.diamondsquare import DiamondSquareAlgorithm

TICKS=350

class DiamondSquare(object):

    def __init__(self, matrix, generate):
        self.diamond = DiamondSquareAlgorithm(matrix.width, matrix.height, (matrix.width+matrix.height)/4)
        self.matrix = OPCMatrix(matrix.width, matrix.height, None, zigzag=matrix.zigzag)
        self.generate = generate
        self.ticks = 0

    def start(self, matrix):
        matrix.clear()

    def refresh(self, matrix):
        # ticks allow us to keep track of how much time has passed
        # since the last generation. This gives us opportunity for
        # both a smooth transition, and time to observe the result
        if self.ticks <= 0 :
            self.generate(self.matrix, self.diamond)
            self.ticks = TICKS

        self.ticks -= 10

        matrix.buf.avg(self.matrix.buf, 0.9)

    def interval(self):
        return 100
