from ._baseclass import ArtBaseClass

import math

from opc.hue import getColorGen


class Art(ArtBaseClass):

    description = "Rolling sine wave marks border between contrasting colors"

    def __init__(self, matrix, config):
        self.hue1 = getColorGen(step=0.00001, hue=0.0)
        self.hue2 = getColorGen(step=0.00001, hue=0.5)

        self.phase = 0

    def start(self, matrix):
        matrix.hq()
        matrix.clear()

    def refresh(self, matrix):
        offset = matrix.midHeight

        for x in range(matrix.width):
            angle = 2 * math.pi * x/matrix.width
            y = matrix.midHeight + \
                matrix.midHeight * math.sin(angle+self.phase)

            matrix.drawLine(x, y, x, y-offset, next(self.hue1))
            matrix.drawLine(x, y, x, y+offset, next(self.hue2))

        self.phase += 0.05

    def interval(self):
        return 100
