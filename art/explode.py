from ._baseclass import ArtBaseClass

from .utils.shrapnel import Shrapnel
from math import sqrt


class Art(ArtBaseClass):

    description = "And then it exploded..."

    PAUSE_CYCLES = 10

    def __init__(self, matrix, config):
        self.pause = 0
        self.pieces = int(sqrt(matrix.numpix))

        cycles = int(sqrt(matrix.numpix)*2)
        self.shrapnel = [Shrapnel(matrix, cycles, decelerate=True)
                         for i in range(self.pieces)]

    def start(self, matrix):
        matrix.clear()

    def _update(self, matrix):
        done = 0
        for shrap in self.shrapnel:
            if shrap.clock(matrix):
                done += 1

        if done == self.pieces:
            for shrap in self.shrapnel:
                shrap.reset(matrix)

            self.pause = self.PAUSE_CYCLES

    def refresh(self, matrix):
        matrix.shift(dv=0.7)
        if self.pause == 0:
            self._update(matrix)
        else:
            self.pause -= 1

    def interval(self):
        return 50
