from opc.matrix import OPCMatrix
from opc.colors import *

from random import randrange

def array(dimensions, initial, depth=0):
    try:
        extent = dimensions[depth]
    except:
        return initial

    return [array(dimensions, initial, depth+1) for y in range(extent)]

class Tetrimino(object):

    """
    This is a play piece. It can't do much other than represent itself

    The piece's shape is determined by a single byte. In a "unrotated"
    state, the top four bits represent the top row, and the bottom four
    the other. So:

                7 6 5 4
                3 2 1 0

    Consider this as a bitstream, where we always unpack in the same order
    and then later on consider how to hydrate that bitstream in any given
    orientation.

    """
    up, right, down, left = 0, 1, 2, 3

    def __init__(self, color, bits):
        self.order = {
                self.up:    { "x": range(0, 4, 1),     "y": range(0, 2, 1),   "dim": (4, 2)},
                self.down:  { "x": range(3, -1, -1),   "y": range(1, -1, -1), "dim": (4, 2)},
                self.left:  { "x": range(0, 2, 1),     "y": range(0, 4, 1),   "dim": (2, 4)},
                self.right: { "x": range(1, -1, -1),   "y": range(3, -1, -1), "dim": (2, 4)},
            }
        self.color = color
        self.bits = bits

    def _stream(self):
        for row in range(2):
            for bit in range(4):
                shift = bit + 4*row
                value = (self.bits >> shift) & 1
                yield value

    def hydrate(self, rotation):

        w, h = self.order[rotation]["dim"]

        block = array([w, h], None)
        stream = self._stream()

        for y in self.order[rotation]["y"]:
            for x in self.order[rotation]["x"]:
                if stream.next():
                    block[x][y] = self.color

        return block

class InPlay(object):

    """
    This is the piece in play, and it takes direction from the game
    """
    def __init__(self, tetriminos, width, height):
        self.tetrimino = tetriminos[randrange(len(tetriminos))]
        self.rotation = 0
        self.x = width/2
        self.y = height

    def rotateClock(self):
        self.rotation = (self.rotation + 1) & 3

    def rotateAnti(self):
        self.rotation = (self.rotation - 1) & 3

    def drop(self, direction):
        self.y += direction

        return self.y

    def modePlace(self, well, x, y, color):
        """
        Place the piece in the well
        """
        well[x][y] = color

        return True

    def modeIsPlacementValid(self, well, x, y, color):
        """
        Check to see if the piece will fit in the well at the current location
        Return False if it does not.
        Special case is if any y value is -1, which means we've fallen off
        the bottom of the board. If this is the case, then the placement isn't
        valid.
        """
        if y < 0 or well[x][y] is not None:
            return False

        return True

    def modeErase(self, well, x, y, color):
        """
        Remove the piece from the well
        """
        well[x][y] = None

        return True

    def operation(self, action, well):
        """
        perform an operation between the well and the piece in play. action
        determines the detail of that operation.
        """
        hydrated = self.tetrimino.hydrate(self.rotation)
        for y in range(len(hydrated[0])):
            for x in range(len(hydrated)):
                color = hydrated[x][y]
                if color is not None:
                    if action(well, self.x-x, self.y-y, color) is False:
                        return False

        return True


class Well(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clear()

    def add(self, tetrimino):
        pass

    def remove(self, tetrimino):
        pass

    def draw(self, matrix):
        for x in range(self.width):
            for y in range(self.height):
                color = self.well[x][y]
                if color is not None:
                    matrix.drawPixel(x, y, color)

    def clear(self):
        self.well = array([self.width, self.height], None)

class Game(object):

    def __init__(self, width, height):
        shapes = { CYAN: 15, BLUE: 142, RY2: 46, YELLOW: 51, GREEN: 54, MAGENTA: 39, RED: 99 }
        self.tetriminos = [ Tetrimino(color, bits) for color, bits in shapes.iteritems() ]

        self.width = width
        self.height = height

        self.well = Well(width, height)
        self.current = self._pick()
        self.finished = False

    def _pick(self):
        return InPlay(self.tetriminos, self.width, self.height-1)

    def clock(self, time):
        """
        Drop the piece by one pixel, check to see if that space is valid. If
        it is, then great. Otherwise the previous position was where the piece
        needs to stick. To make this check work, we need to delete the piece
        from the well in the existing location first.

        The exception is that if this is the first time the piece has been
        laid down and it doesn't fit, then the well is full and the game is
        over.
        """
        c = self.current # handy shorthand

        c.operation(c.modeErase, self.well.well)
        c.drop(-1)
        if c.operation(c.modeIsPlacementValid, self.well.well):
            c.operation(c.modePlace, self.well.well)
        else:
            if c.drop(1) == self.height-1:
                self.finished = True

            c.operation(c.modePlace, self.well.well)
            self.current = self._pick()

    def draw(self, matrix):
        self.well.draw(matrix)

class Art:

    description = "Anyone for a game of Tetris?"

    def __init__(self, matrix):
        self._newGame()

    def _newGame(self):
        self.game = Game(10, 16)
        self.time = 0

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)

    def refresh(self, matrix):
        matrix.clear()

        self.time += 1
        self.game.clock(self.time)
        self.game.draw(matrix)

        if self.game.finished:
            self._newGame()

        self.game.draw(matrix)
  
    def interval(self):
        return 200

