from math import sin, cos, sqrt

from opc.colors import BLACK
from opc.hue import getColorGen

SCALE = 4


class Art(object):

    description = "Demo image rotation"

    def __init__(self, matrix):
        self.hue = getColorGen(0.006)
        self.margin = sqrt(matrix.numpix) * 0.7

    def start(self, matrix):
        matrix.hq(True)

    def refresh(self, matrix):

        color = self.hue.next()
        matrix.fillPoly([
            (matrix.width/2, self.margin),
            (self.margin, matrix.height-self.margin),
            (matrix.width-self.margin, matrix.height-self.margin),
            ], color
            )
        #matrix.fillRect(self.margin, self.margin, matrix.width-2*self.margin,
                #matrix.height-2*self.margin, color)
        matrix.rotate(5)

    def interval(self):
        return 80
