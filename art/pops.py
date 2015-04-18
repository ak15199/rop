from _baseclass import ArtBaseClass

from utils.shrapnel import Shrapnel
from math import sqrt


class Art(ArtBaseClass):

    description = "Bubbling pixels"

    def __init__(self, matrix):
        self.pieces = int(sqrt(matrix.numpix))

        cycles = int(sqrt(matrix.numpix)*2)
        self.shrapnel = [Shrapnel(matrix, cycles, saturation=0.2) for i in range(self.pieces)]

    def start(self, matrix):
        matrix.clear()

    def refresh(self, matrix):
        matrix.fade(0.7)

        for shrap in self.shrapnel:
            if shrap.clock(matrix):
                shrap.reset(matrix)

    def interval(self):
        return 50
