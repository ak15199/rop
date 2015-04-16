from math import radians, sqrt, sin, cos, ceil
from random import random
from opc.colors import WHITE
from opc.hue import getHueGen, hsvToRgb
from opc.matrix import OPCMatrix


class Point(object):

    def __init__(self, x, y):
        self.x, self.y = x, y

    def coords(self):
        return self.x, self.y


class Art(object):

    description = "Kaleidoscope"

    FITHALF = 0.45 # squeeze radius into 90% of display area

    def __init__(self, matrix):
        self.angle = 0
        self.hue = getHueGen(0.01)
        self.radius = sqrt(matrix.numpix) * self.FITHALF
        self.center = Point(matrix.midWidth, matrix.midHeight)
        self.pieslice = self._pieslice(-30, 30)

        # used to help with scaling small displays
        # freq will have a value of 1 for kilopix displays and hold a
        # larger value for smaller displays (up to 4)
        self.freq = min(4, max(1, 1024.0/matrix.numpix))
        self.clock = 0

        # create mask
        self.mask = OPCMatrix(matrix.width, matrix.height, None)
        self.mask.fillPoly(self.pieslice, WHITE)
        matrix.fillPoly(self.pieslice, WHITE)

        # create intermediate buffers
        self.intermediate1 = OPCMatrix(matrix.width, matrix.height, None)
        self.intermediate2 = OPCMatrix(matrix.width, matrix.height, None)

        # create private buffer for final rendering before rotate/display
        self.private = OPCMatrix(matrix.width, matrix.height, None)

    def _offset(self, angle):
        return Point(
                    self.center.x+self.radius*sin(radians(angle)),
                    self.center.y+self.radius*cos(radians(angle)),
                )

    def _pieslice(self, offset1, offset2):
        return [
                self._offset(offset1).coords(),
                self._offset(offset2).coords(),
                self.center.coords(),
                ]

    def start(self, matrix):
        pass

    def _draw(self, matrix):
        x = matrix.width*random()
        y = self.center.y + (self.pieslice[0][1]-self.center.y)*random()
        z = 2 + random()*10/self.freq

        if random()<0.1:
            color = WHITE
        else:
            offset = int(random()*4)/4.0 if random()<0.5 else 0
            color = hsvToRgb(offset+self.hue.next(), 1, 1)

        if random()<0.5:
            matrix.drawRect(x, y, z, z, color)
        else:
            matrix.fillRect(x, y, z, z, color)

    def _update(self, matrix):
        self.clock += 1
        if self.clock % ceil(self.freq/2.0) == 0:
            if self.clock % self.freq == 0:
                matrix.copy(matrix, 1, 0)
            for draws in range(5-self.freq):
                self._draw(matrix)

    def refresh(self, matrix):
        #
        # use a copy-flip-rotate strategy to build a set of mirrored segments
        #

        # modify the display
        self._update(self.private)

        # we just want the top 1/6th pie slice to start
        self.private.mask(self.mask)

        # the other slices need to be reversed (see later)
        self.private.flip(lr=True)

        # create the left and right pie slices
        self.intermediate1.copy(self.private)
        self.intermediate1.rotate(60)

        self.intermediate2.copy(self.private)
        self.intermediate2.rotate(-60)

        # the original needs to be flipped back to its original state
        # if it isn't then there'll be flip-flopping between frames
        self.private.flip(lr=True)

        # drop the slices into the (flipped) original
        self.private.add(self.intermediate1)
        self.private.add(self.intermediate2)

        # the other half is a mirror of what we already have
        self.intermediate1.copy(self.private)
        self.intermediate1.flip(ud=True)

        # drop the mirror onto the matrix
        self.private.add(self.intermediate1)
        self.private.flip(ud=True)

        matrix.copy(self.private)

        self.angle -= 1
        matrix.rotate(self.angle)

    def interval(self):
        if self.freq>2:
            return 200
        else:
            return 150
