from ._baseclass import ArtBaseClass
from opc.hue import hsvToRgb

import numpy as np

import random
import math

class Art(ArtBaseClass):

    description = "Voronoi Animation"

    def __init__(self, matrix, config):
        self.field = None
        self.count = int(math.sqrt(matrix.numpix)/3)
        self.regions = self._seed(matrix)
        self.huebase = 0

    def _delta(self, size):
        r = math.sqrt(size)/5

        d = 0
        while not d:
            d = random.uniform(-r, r)

        return d

    def _seed(self, matrix):
        return [{
                "nx": random.randrange(matrix.width),
                "ny": random.randrange(matrix.height),

                "ndx": self._delta(matrix.width),
                "ndy": self._delta(matrix.height),
                } for i in range(self.count)]

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)
        matrix.hq()
        matrix.clear()

    def _bounce(self, v, s, vmin, vmax):
        if v<=vmin:
            return abs(s)
        if v>=vmax:
            return -abs(s)
        return s

    def refresh(self, matrix):
        self.huebase = self.huebase + 0.001

        field = np.empty((matrix.width, matrix.height))

        for y in range(matrix.height):
            for x in range(matrix.width):
                dmin = math.hypot(matrix.width-1, matrix.height-1)
                j = -1
                for i in range(self.count):
                    d = math.hypot(self.regions[i]["nx"]-x, self.regions[i]["ny"]-y)
                    if d < dmin:
                        dmin = d
                        j = i

                field[x,y] = self.huebase+j/self.count

        self.regions = [{
                "nx": region["nx"]+region["ndx"],
                "ny": region["ny"]+region["ndy"],

                "ndx": self._bounce(region["nx"], region["ndx"], 0, matrix.width),
                "ndy": self._bounce(region["ny"], region["ndy"], 0, matrix.height),
                } for region in self.regions]

        if self.field is not None:
            self.field = (self.field*0.3) + (field*0.7)
        else:
            self.field = field

        for y in range(matrix.height):
            for x in range(matrix.width):
                matrix.drawPixel(x, y, hsvToRgb(self.field[x,y], 1, 1))

     
    def interval(self):
        return 100
