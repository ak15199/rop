from _baseclass import ArtBaseClass

from opc.colors import GRAY40, WHITE, RED

from copy import deepcopy
from random import randrange, shuffle


MZ_FREE = {"name": "Free", "color": GRAY40}
MZ_WALL = {"name": "Wall", "color": WHITE}
MZ_PATH = {"name": "Path", "color": None}  # chosen on the fly
MZ_DOOR = {"name": "Door", "color": RED}
MZ_SCAF = {"name": "Scaf", "color": GRAY40}  # scaffold

MZ_PRIMARIES = [
    (192, 0, 0),
    (192, 192, 0),
    (0, 192, 0),
    (0, 0, 192),
    (0, 192, 192)
    ]


class Art(ArtBaseClass):

    description = "Recursive backtracking maze generation"

    """
    See http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-
    backtracking

    for a rough idea on how this works. That approach assumes that walls
    can be represented on a per-cell basis, which doesn't really work in
    our case.  So we have a little extra work to do in that cells can
    either be path elements or wall elements.

    XXX: there's a problem here, in that it really only looks ok for odd
    number of cells in each direction (because of the scaffold). For now,
    we fudge it and subtract one from the (assumed) even number of cells in
    each direction, but this needs some work.
    """

    def __init__(self, matrix):
        self.width = matrix.width - 1
        self.height = matrix.height - 1
        self.matrix = matrix.clone()
        self.initialized = False

        self.directions = [
            {"x": 0,  "y": 1,  "name": "N"},
            {"x": 0,  "y": -1, "name": "S"},
            {"x": 1,  "y": 0,  "name": "E"},
            {"x": -1, "y": 0,  "name": "W"},
            ]

        self.mode = self._mode_draw

    def start(self, matrix):
        if not self.initialized:
            self._initialize_map(matrix)
            self._seed_queue(matrix)
            self.initialized = True

        matrix.copy(self.matrix)

    def _initialize_map(self, matrix):
        self.steps = []

        self.maze = [[MZ_FREE for y in range(self.height)]
                     for x in range(self.width)]
        self.matrix.clear(MZ_FREE["color"])

        shuffle(MZ_PRIMARIES)
        MZ_PATH["color"] = MZ_PRIMARIES[0]

        # build a scaffold that the paths will run amongst.
        for x in range(1, self.width, 2):
            for y in range(1, self.height, 2):
                self._mark(matrix, x, y, MZ_SCAF)

    def _seed_queue(self, matrix):
        self._step(matrix, 0, randrange(3, self.height-3))

    def _mark(self, matrix, x, y, type):
        self.maze[x][y] = type
        self.matrix.drawPixel(x, y, type["color"])
        matrix.drawPixel(x, y, type["color"])

    def _inrange(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def _isType(self, x, y, t):
        return self._inrange(x, y) and self.maze[x][y] == t

    def _isFree(self, x, y):
        return self._isType(x, y, MZ_FREE)

    def _isPath(self, x, y):
        return self._isType(x, y, MZ_PATH)

    def _isWall(self, x, y):
        return self._isType(x, y, MZ_WALL)

    def _isScaf(self, x, y):
        return self._isType(x, y, MZ_SCAF)

    def _causesPathLoop(self, x, y):
        count = 0
        for direction in self.directions:
            nx, ny = x + direction["x"], y + direction["y"]
            if self._isPath(nx, ny):
                count += 1
                if count == 2:
                    return True

        return False

    def _step(self, matrix, x, y):
        # prelim: if the cell is a scaffold, then turn it into a wall
        if self._isScaf(x, y):
            self._mark(matrix, x, y, MZ_WALL)

        # prelim: if the cell is occupied, then we're done
        if not self._isFree(x, y):
            return False

        # first, we make sure we have a random order of operations
        shuffle(self.directions)
        directions = deepcopy(self.directions)

        # second, we mark the cell in the map
        self._mark(matrix, x, y, MZ_PATH)

        # third, we check for neighbors that could bridge the path if a
        # connection is added
        for direction in directions:
            nx, ny = x + direction["x"], y + direction["y"]
            if self._isFree(nx, ny) and self._causesPathLoop(nx, ny):
                self._mark(matrix, nx, ny, MZ_WALL)

        # forth, we add new places to explore to the stack
        for direction in directions:
            nx, ny = x + direction["x"], y + direction["y"]
            self.steps.append((nx, ny))

        return True

    def _mode_draw(self, matrix):
        try:
            working = False
            while not working:
                x, y = self.steps.pop()
                working = self._step(matrix, x, y)
        except IndexError:  # when we've run out of elements
            self.mode = self._mode_cleanup

    def _mode_cleanup(self, matrix):
        # the algorithm doesn't fill scaf cells that are surrounded by walls
        # so need to go back and fix that after the fact.
        for x in range(self.width):
            for y in range(self.height):
                if self._isScaf(x, y):
                    self._mark(matrix, x, y, MZ_WALL)

        self.counter = 20
        self.mode = self._mode_pause

    def _mode_pause(self, matrix):
        self.counter -= 1
        if self.counter == 0:
            self.mode = self._mode_restart

    def _mode_restart(self, matrix):
        self.initialized = False
        self.start(matrix)
        self.mode = self._mode_draw

    def refresh(self, matrix):
        self.mode(matrix)

    def interval(self):
        return 100
