from random import random, randrange
from math import sqrt
from utils.pen import Pen


class Art(object):

    description = "Rain falling down the display"

    def __init__(self, matrix):
        hue = random()
        pencount = int(sqrt(matrix.width*matrix.height/2))

        self.pens = []
        for pen in range(pencount):
            speed = (1.0+pen)/pencount

            # height is longer than the height of the screen, so drops stay
            # off screen for a little while
            height = int(matrix.height*1.3)

            pen = Pen(
                matrix.width, height,
                randrange(matrix.width), height,
                0, -speed,
                hue=hue,
                persist=False)

            pen.setValue(speed)
            pen.setBumpStrategy(pen.random, x=True)
            pen.setBumpStrategy(pen.reset, y=True)

            self.pens.append(pen)

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)
        matrix.clear()

    def refresh(self, matrix):
        for pen in self.pens:
            pen.clock(matrix)

    def interval(self):
        return 60
