from opc.matrix import OPCMatrix

from random import random, randrange
from math import fmod

from utils.pen import Pen

PENS = 4

class Art(object):

    description = "Bouncy balls with trail"

    def __init__(self, matrix):
        self.pens = [
                Pen(matrix.width, matrix.height, 2, 3, 1.0, 1.1),
                Pen(matrix.width, matrix.height, 5, 0, 1.2, 1.0),
                Pen(matrix.width, matrix.height, 8, 15, 0.9, 1.1),
                Pen(matrix.width, matrix.height, 14, 1, 1.0, 0.9),
            ]

        for pen in self.pens:
            pen.setBumpStrategy(pen.reverse, x=True, y=True)

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)
        matrix.clear()

    def refresh(self, matrix):
        for pen in self.pens:
            pen.clock(matrix)
  
    def interval(self):
        return 100

