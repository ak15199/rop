from opc.matrix import OPCMatrix

from random import random, randrange
from math import fmod
from utils.pen import Pen

PENS = 8

class Art:

    def __init__(self, matrix):
        hue = random()
        self.pens = []
        for pen in range(PENS):
            speed = (1.0+pen)/PENS

            # height is longer than the height of the screen, so drops stay away for a little while
            height = int(matrix.height()*1.3)

            pen = Pen(matrix.width(), height, 0, randrange(matrix.height()), speed, 0, persist=False)
            pen.setValue(speed)
            pen.setBumpStrategy(pen.randomreset, x=True)
            pen.setBumpStrategy(pen.none, y=True)
            self.pens.append(pen)

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)
        matrix.clear()

    def refresh(self, matrix):
        for pen in self.pens:
            pen.clock(matrix)
  
    def interval(self):
        return 60

