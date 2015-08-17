from _baseclass import ArtBaseClass

from opc import colors
from opc.hue import hsvToRgb

from math import sqrt
import operator
from random import shuffle, random


class Art(ArtBaseClass):

    description = "Seeping spill color across the display"

    def __init__(self, matrix, config):
        self.width = matrix.width
        self.height = matrix.height
        self.perCycle = sqrt(matrix.numpix)/4
        self.deltaValue = 3.0/matrix.numpix

        self.offsets = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    def start(self, matrix):
        matrix.clear((128+64,128+64,128+64))#colors.WHITE)
        self._initialize(matrix)

    def _initialize(self, matrix):
        self.value = 1
        self.hue = random()
        self.filling = {}
        self.full = []

        addr = self._encode(int(self.width*random()),
                            int(self.height*random()))
        self._setCell(matrix, addr, 0)

    def _encode(self, x, y):
        return "%s|%s" % (x, y)

    def _decode(self, addr):
        return [int(v) for v in addr.split("|")]

    def _cellIsValid(self, x, y):
        return x >= 0 and y >= 0 and x < self.width and y < self.height

    def _getNewNeighbor(self, cell):
        # find a neighbor to this cell that is empty
        shuffle(self.offsets)
        here = self._decode(cell)

        for offset in self.offsets:
            x, y = map(operator.add, here, offset)
            if self._cellIsValid(x, y):
                addr = self._encode(x, y)
                if addr in self.full or addr in self.filling:
                    continue

                return addr

        return None

    def _updateNeighbors(self, cell):
        # let each of our neighbors know that there's a new guy in town
        neighbors = 0
        here = self._decode(cell)

        for offset in self.offsets:
            x, y = map(operator.add, here, offset)
            addr = self._encode(x, y)
            if self._cellIsValid(x, y) and addr in self.filling:
                count = self.filling[addr]
                neighbors += 1
                if count == 3:
                    self.full.append(addr)
                    del self.filling[addr]
                else:
                    self.filling[addr] += 1

        return neighbors

    def _setCell(self, matrix, addr, neighbors):
        x, y = self._decode(addr)
        matrix.drawPixel(x, y, hsvToRgb(self.hue, 1, 1), self.value)
        self.filling[addr] = neighbors
        self.value -= self.deltaValue

        return self.value <= 0

    def refresh(self, matrix):
        keys = self.filling.keys()
        count = min(self.perCycle, len(keys))
        shuffle(keys)

        for key in keys:
            neighbor = self._getNewNeighbor(key)
            if neighbor is None:
                continue

            neighbors = self._updateNeighbors(neighbor)
            expired = self._setCell(matrix, neighbor, neighbors)
            if expired:
                self._initialize(matrix)
                return

            count -= 1
            if count == 0:
                return

    def interval(self):
        return 50
