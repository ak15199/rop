from random import random

from opc.hue import getHueGen
from opc.matrix import OPCMatrix

from utils.frange import frandrange
from utils.pen import Pen

PENS = 4
SCALE = 4
SIZE = 6

class Art(object):

    description = "Bouncing blobs"

    def __init__(self, matrix):
        self.matrix = OPCMatrix(SCALE*matrix.width, SCALE*matrix.height, None,
                True)

        self.pens = []
        for i in range(PENS):
            dx = 1 if (i/2)%2 == 0 else -1
            dy = 1 if i%2 == 0 else -1
            pen = Pen(
                    self.matrix.width, self.matrix.height,
                    self.matrix.width/4 + random()*self.matrix.width/2,
                    self.matrix.height/4 + random()*self.matrix.height/2,
                    dx=dx, dy=dy, radius=self.matrix.width/SIZE,
                    huedelta=frandrange(0.005, 0.001),
                    )
            pen.setBumpStrategy(pen.reverse, x=True, y=True)
            self.pens.append(pen)

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        self.matrix.clear()

        for pen in self.pens:
            pen.clock(self.matrix)

        matrix.copy(self.matrix)
  
    def interval(self):
        return 80

