from opc.matrix import OPCMatrix
from opc.colors import *

from time import sleep
from random import randrange, random, shuffle

MZ_FREE = { "name": "Free", "color": (156, 156, 156) }
MZ_WALL = { "name": "Wall", "color": BLUE }
MZ_PATH = { "name": "Path", "color": WHITE }
MZ_DOOR = { "name": "Door", "color": RED }

# with some help from
# http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking
#

class Art:

    def __init__(self, matrix):
        self.debug = True
        self.width = matrix.width
        self.height = matrix.height
        self.matrix = matrix
        self.directions = [ 
                { "x": 0,  "y": 1,  "name": "N" },
                { "x": 0,  "y": -1, "name": "S" }, 
                { "x": 1,  "y": 0,  "name": "E" }, 
                { "x": -1, "y": 0,  "name": "W" }, 
            ]

    def start(self, matrix):
        matrix.clear(WHITE)
        self._initialize()

    def _mark(self, x, y, type):
        self.maze[x][y] = type
        self.matrix.drawPixel(x, y, type["color"])
        self.matrix.show()

        if self.debug: print "set (x, y) = type", x, y, self.maze[x][y]["name"]
        
    def _initialize(self):
        self.maze = [ [MZ_FREE for x in range(self.width)] for y in range(self.height)]
        self.matrix.fillRect(0, 0, self.width, self.height, MZ_FREE["color"])
        """
        for x in range(self.width):
            self._mark(x, 0, MZ_WALL)
            self._mark(x, self.height-1, MZ_WALL)

        for y in range(self.height):
            self._mark(0, y, MZ_WALL)
            self._mark(self.width-1, y, MZ_WALL)
        """

    def _inrange(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def _isFree(self, x, y): return self._inrange(x, y) and self.maze[x][y] == MZ_FREE
    def _isPath(self, x, y): return self._inrange(x, y) and self.maze[x][y] == MZ_PATH
    def _isWall(self, x, y): return self._inrange(x, y) and self.maze[x][y] == MZ_WALL

    def _same(self, x1, y1, x2, y2):
        return x1 == x2 and y1 == y2

    def _wallCandidate(self, x, y, trigPaths, trigWalls, ex, ey):
        walls, paths = 0, 0

        if not self._isFree(x, y):
            return False

        for direction in self.directions:
            nx, ny = x + direction["x"], y + direction["y"]
            if self._same(ex, ey, nx, ny) or not self._inrange(nx, ny):
                continue

            isPath = self._isPath(nx, ny)
            if isPath: paths += 1
            isWall = self._isWall(nx, ny)
            if isWall: walls += 1
            
            if self.debug: print "      check (x, y, v) [ip, iw]", nx, ny, self.maze[nx][ny]["name"], isPath, isWall

            if (walls >= trigWalls and trigWalls is not None) or    \
                    (paths >= trigPaths and trigPaths is not None):
                print "        -> return true"
                return True 
            
        print "        -> return false"
        return False

    def _extendPath(self, x, y):
        # set the specified cell to be path
        sleep(.1)

        self._mark(x, y, MZ_PATH)

        # XXX: don't use trigWalls any more, can refactor out
        # XXX: explain new model

        # XXX: ALMOST!
        # exception: should never extend a wall (the recursive step)
        # if that square is adjacent to an upstream item... we will worry
        # about that later
        self._extendWall(x, y, True, 2, None)

    def _extendWall(self, x, y, recurse, trigPaths, trigWalls):
        if self.debug: print "extendwall: begin"
        for neighbor in self.directions:
            nx, ny = x + neighbor["x"], y + neighbor["y"]
            if self.debug: print "   ", x, y, "->", nx, ny
            if self._wallCandidate(nx, ny, trigPaths, trigWalls, nx, ny):
                if self.debug: print "extendwall: build wall"
                self._mark(nx, ny, MZ_WALL)
                if recurse:
                    if self.debug: print "extendwall: trying neighbors"
                    self._extendWall(nx, ny, False, 2, 3)

    def _build(self, cx, cy, serial):
        self._extendPath(cx, cy)
        shuffle(self.directions)
        for direction in self.directions:
            nx, ny = cx + direction["x"], cy + direction["y"] 
            print "serial ", serial, " (x,y) = v [free]", nx, ny, direction["name"], self._isFree(nx, ny)
            if self._isFree(nx, ny):
                self._build(nx, ny, serial +1)

    def refresh(self, matrix):
        self._build(0, randrange(3, self.height-3), 1000)
        exit()

    def interval(self):
        return 400

