import math

from opc.hue import getColorGen
from opc.scaledmatrix import ScaledMatrix


class Art(object):

    description = "Rolling sine wave marks border between contrasting colors"

    def __init__(self, matrix):
        self.matrix = ScaledMatrix(matrix, scale=2)
        self.hue1 = getColorGen(step=0.00001, hue=0.0)
        self.hue2 = getColorGen(step=0.00001, hue=0.5)

        self.phase = 0

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        offset = self.matrix.scale * 1.2

        for x in range(self.matrix.width):
            angle = 2 * math.pi * x/self.matrix.width
            y = self.matrix.midHeight + \
                self.matrix.midHeight * math.sin(angle+self.phase)

            self.matrix.drawLine(x, y, x, y-offset, self.hue1.next())
            self.matrix.drawLine(x, y, x, y+offset, self.hue2.next())

        self.phase += 0.05

        self.matrix.scaleDown()

    def interval(self):
        return 100
