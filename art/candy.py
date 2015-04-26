from _baseclass import ArtBaseClass

from utils.shrapnel import Shrapnel
from math import sqrt
from random import random

from opc.matrix import HQ


class Art(ArtBaseClass):

    description = "Churning candy"

    def __init__(self, matrix, config):
        with HQ(matrix):
            self.pieces = int(sqrt(matrix.numpix))

            cycles = int(sqrt(matrix.numpix)*2)
            self.shrapnel = [Shrapnel(matrix, cycles, saturation=random(),
                             radius=5) for i in range(self.pieces)]

            for shrap in self.shrapnel:
                shrap.dx = 8
                shrap.dy = 8

    def start(self, matrix):
        matrix.hq()
        matrix.clear()

    def refresh(self, matrix):
        matrix.fade(0.7)

        for shrap in self.shrapnel:
            if shrap.clock(matrix):
                shrap.reset(matrix)

    def interval(self):
        return 50
