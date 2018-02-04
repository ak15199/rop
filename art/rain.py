from _baseclass import ArtBaseClass

from random import random, randrange
from math import sqrt
from utils.pen import Pen

from opc.matrix import HQ


class Art(ArtBaseClass):

    description = "Rain falling down the display"

    def __init__(self, matrix, config):
        with HQ(matrix):
            hue = random()
            pencount = int(sqrt(matrix.width*matrix.height/2))

            self.pens = []
            for pen in range(pencount):
                speed = float(2*pen)/pencount

                # height is longer than the height of the screen, so drops stay
                # off screen for a little while
                height = int(matrix.height*1.1)

                pen = Pen(
                    matrix.width, height,
                    randrange(matrix.width), height,
                    0, -speed,
                    hue=hue,
                    radius=4,
                    persist=False)

                pen.setValue(speed)
                pen.setBumpStrategy(pen.random, x=True)
                pen.setBumpStrategy(pen.reset, y=True)

                self.pens.append(pen)

    def start(self, matrix):
        matrix.hq()

    def refresh(self, matrix):
        for pen in self.pens:
            pen.clock(matrix)

    def interval(self):
        return 90
