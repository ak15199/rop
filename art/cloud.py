from opc.matrix import OPCMatrix
from random import random
from opc.hue import hsvToRgb, getHueGen
from basecls.diamondsquare import DiamondSquare

class Art(object):

    description = "Clouds drawn with the diamond square algorithm"

    """
    ported from http://www.bluh.org/code-the-diamond-square-algorithm/
    """
    def __init__(self, matrix):
        self.diamond = DiamondSquare(matrix.width, matrix.height, (matrix.width+matrix.height)/4)

        self.matrix = OPCMatrix(matrix.width, matrix.height, None, zigzag=matrix.zigzag)
        self.ticks = 100
        self.hue = 0.1

    def start(self, matrix):
        matrix.clear()

    def refresh(self, matrix):
        # ticks allow us to keep track of how much time has passed
        # since the last generation. This gives us opportunity for
        # both a smooth transition, and time to observe the result
        if self.ticks == 350:
            self.diamond.generate(self.matrix, hue=self.hue)
            self.hue += 0.01
            self.ticks = 0

        self.ticks += 10

        matrix.buf.avg(self.matrix.buf, 0.9)

    def interval(self):
        return 100
