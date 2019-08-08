from ._baseclass import ArtBaseClass
from opc.hue import hsvToRgb

import numpy as np

import random
import math


class Art(ArtBaseClass):

    description = "Voronoi Animation"

    def __init__(self, matrix, config):
        self.field = None
        self.count = int(math.sqrt(math.sqrt(matrix.numpix)))
        self.regions = self._seed(matrix)
        self.huebase = 0

    def _delta(self, size):
        r = 0.1
        d = 0
        while not d:
            d = random.uniform(-r, r)

        return d

    def _seed(self, matrix):
        return [{
                "x": random.randrange(matrix.width),
                "y": random.randrange(matrix.height),

                "dx": self._delta(matrix.width),
                "dy": self._delta(matrix.height),
                } for i in range(self.count)]

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)
        matrix.clear()

    def _bounce(self, v, step, vmax):
        if v<=1:
            return abs(step)
        if v>=vmax-step:
            return -abs(step)

        return step

    def _closest(self, xs, ys, x, y):
        hypots = np.hypot(xs-x, ys-y)

        return np.where(hypots == np.amin(hypots))[0][0]

    def refresh(self, matrix):
        self.huebase = self.huebase + 0.001

        # canvas for us to write to
        field = np.empty((matrix.width, matrix.height))

        # linearize x and y coordinates for regions
        xs = np.array([region["x"] for region in self.regions])
        ys = np.array([region["y"] for region in self.regions])

        # find closest region to eack pixel
        for y in range(matrix.height):
            for x in range(matrix.width):
                c=self._closest(xs, ys, x, y)
                field[x,y] = self.huebase+c/self.count

        # update region coordinates
        self.regions = [{
                "dx": self._bounce(region["x"], region["dx"],  matrix.width-1),
                "dy": self._bounce(region["y"], region["dy"],  matrix.height-1),

                "x": region["x"]+region["dx"],
                "y": region["y"]+region["dy"],
            } for region in self.regions]

        # blend old and new
        if self.field is not None:
            self.field = (self.field*0.3) + (field*0.7)
        else:
            self.field = field

        # draaw
        for y in range(matrix.height):
            for x in range(matrix.width):
                matrix.drawPixel(x, y, hsvToRgb(self.field[x,y], 1, 1))

        for region in self.regions:
            matrix.drawPixel(region["x"], region["y"], hsvToRgb(1,  0, 0))

    def interval(self):
        return 50
