from opc.matrix import OPCMatrix
from opc.colors import *

from random import randrange, random

MZ_FREE = 0
MZ_WALL = 1
MZ_PATH = 2
MZ_DOOR = 3

# This is a work in progress

class Art:

    def __init__(self, matrix):
        self.width = matrix.width
        self.height = matrix.height

    def start(self, matrix):
        matrix.clear(WHITE)
        self._initialize():

    def _initialize(self):
        self.maze = [[MZ_FREE for x in range(self.width)] for y in range(self.height)]
        for x in range(self.width):
            self.maze[x][0] = MZ_WALL
            self.maze[x][self.height-1] = MZ_WALL

        for y in range(self.height):
            self.maze[0][y] = MZ_WALL
            self.maze[self.width-1][y] = MZ_WALL

        self.path = []
        self.here = (0, randrange(3, matrix.height-3)

    def _unwind(self):
        pass

    def _build(self):
        pass

    def refresh(self, matrix):
        self.build()

    def interval(self):
        return 400

