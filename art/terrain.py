from _baseclass import ArtBaseClass

from collections import OrderedDict
from math import sin, cos

from opc.colormap import Colormap
from opc.colors import rgb
from opc.matrix import OPCMatrix
from random import random

from utils.diamondsquare import DiamondSquareAlgorithm


SCALE = 8
CENTERZONE = 16


class Art(ArtBaseClass):

    description = "Traverse procedurally generated terrain"

    def __init__(self, matrix):
        self.width = matrix.width*SCALE
        self.height = matrix.height*SCALE

        self.matrix = OPCMatrix(self.width, self.height, None)
        self.diamond = DiamondSquareAlgorithm(self.matrix.width,
                                              self.matrix.height,
                                              (self.matrix.width +
                                               self.matrix.height) / 4)
        self.colormap = Colormap(palette=OrderedDict([
            (rgb["NavyBlue"], 20),
            (rgb["blue"], 15),
            (rgb["yellow3"], 5),
            (rgb["LawnGreen"], 10),
            (rgb["ForestGreen"], 20),
            (rgb["gray50"], 15),
            (rgb["snow1"], 5),
            ]))

        self.diamond.generate()
        self.diamond.translate(self.matrix, colormap=self.colormap)
        self.matrix.blur()

        self.theta = 0
        self.radius = 0

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)

    def refresh(self, matrix):
        # XXX:
        # The change in angle per frame increases as we get closer to the
        # center of the matrix:
        #  - when radius is max, then deltatheta is about .005 radians.
        #  - when radius is min, then deltatheta is about .1 radians.
        deltatheta = 0.01
        self.theta += deltatheta
        self.radius -= 0.05

        if self.radius < CENTERZONE:
            self.radius = (self.width+self.height)/4

        x = self.width/2 + self.radius * sin(self.theta)
        y = self.height/2 + self.radius * cos(self.theta)

        matrix.copy(self.matrix, x, y)

    def interval(self):
        return 60
