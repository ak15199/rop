from opc.matrix import OPCMatrix
from opc.hue import hsvToRgb
from math import sin, cos
from utils.frange import frange
from utils.fractools import Mandelbrot, Region

from copy import copy
from random import randrange, random

ZOOMSTEPS = 24
ITERSTEPS = 30
DEBUG = False

class Art:

    def __init__(self, matrix):
        self.mandel = Mandelbrot(matrix.width, matrix.height, ITERSTEPS)
        # this gives a pretty good view of the artifact at max zoom
        self.origin = Region(-2.0, -1.5, 1.0, 1.5)
        self._begin(matrix)

        self.i = 0

    def start(self, matrix):
        #matrix.setFirmwareConfig(nointerp=True)
        pass

    def _begin(self, matrix):
        self.target = copy(self.origin)

        self.current = copy(self.target)
        self.delta = Region(0.000000, 0.000000, -0.093750, -0.093750)

        self.stateExecute = self._drawBig
        self.stepsDown = 0
        self._render(matrix, self.target)

    def _text(self, grid):
        map = [ "X", "x", "O", "o", "+", "-", "'", ",", "." ]
        for x in grid:
            for y in x:
                if y is None or y>=9:
                    print " ",
                elif y<9:
                    print map[y],
            print

    def _render(self, matrix, target):
        grid = self.mandel.draw(target)

        matrix.clear()

        for x in range(matrix.width):
            for y in range(matrix.height):
                point = grid[x][y]
                if point is not None:
                    hue = (0.0+point)/self.mandel.maxsteps
                    matrix.drawPixel(x, y, hsvToRgb(hue))
                    
    def _forward(self):
        self.stepsDown += 1
        self.zoomRemaining = ZOOMSTEPS
        self.delta = self.current.delta(self.target, ZOOMSTEPS)

    def _reverse(self):
        self.target = copy(self.origin)
        self.zoomRemaining = self.stepsDown * ZOOMSTEPS/4
        self.delta = self.current.delta(self.origin, self.zoomRemaining)

    def _drawBig(self, matrix):
        """
        draw, then figure out which is the most interesting
        """
        self.current = copy(self.target)
        self.target = self.mandel.mostInteresting(self.target)
        if self.target is None:
            self._reverse()
        else:
            self._forward()

        if DEBUG: print " Origin:", self.origin
        if DEBUG: print "   From:", self.current
        if DEBUG: print "     To:", self.target
        if DEBUG: print "  Steps:", self.delta

        # move to next state
        return self._zoomToTarget(matrix)

    def _zoomToTarget(self, matrix):
        """
        iteratively zoom towards the target until we fill the display
        """
        if self.zoomRemaining:
            self.current.increment(self.delta)
            self._render(matrix, self.current)
            self.zoomRemaining -= 1
            return self._zoomToTarget

        # when we have reached our target, begin the process over
        return self._drawBig

    def refresh(self, matrix):
        self.stateExecute = self.stateExecute(matrix)
  
    def interval(self):
        return 100

