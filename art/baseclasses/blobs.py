from .. _baseclass import ArtBaseClass

from random import random, uniform

from opc.matrix import HQ

from .. utils.pen import Pen

PENS = 4
SCALE = 3
SIZE = 6


class Blobs(ArtBaseClass):

    def __init__(self, matrix):
        with HQ(matrix):
            self.pens = []
            for i in range(PENS):
                dx = 1 if (i/2) % 2 == 0 else -1
                dy = 1 if i % 2 == 0 else -1
                pen = Pen(
                    matrix.width, matrix.height,
                    matrix.width/4 + random()*matrix.width/2,
                    matrix.height/4 + random()*matrix.height/2,
                    dx=dx, dy=dy, radius=matrix.width/SIZE,
                    huedelta=uniform(0.005, 0.001),
                    )
                pen.setBumpStrategy(pen.reverse, x=True, y=True)
                self.pens.append(pen)

    def start(self, matrix):
        matrix.clear()
        matrix.hq()

    def interval(self):
        return 100
