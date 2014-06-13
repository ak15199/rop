from opc.colors import rgb 
from opc.matrix import OPCMatrix

from random import randrange, random
from math import copysign

class Score:

    # condensed numeric characters, with two rows of pixels
    # per byte in a 4x6 grid
    charmap = [
        (105, 153, 150), # 0
        (38, 34, 39), # 1
        (105, 18, 79), # 2
        (105, 33, 150), # 3
        (136, 170, 242), # 4
        (248, 241, 150), # 5
        (120, 233, 150), # 6
        (241, 36, 68), # 7
        (105, 105, 150), # 8
        (105, 113, 22), # 9
        ]

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.score = 0
        self.color = color
        self.win_thresh = 9

    def reset(self):
        self.score = 0

    def bump(self):
        self.score += 1
        return self.score > self.win_thresh

    def _draw(self, matrix, y, line):
        x = self.x 
        while line > 0:
            if line & 1:
                matrix.drawPixel(x, y, self.color)
            line = line >> 1
            x += 1

    def display(self, matrix):
        bytes = self.charmap[self.score]
        y = self.y
        for byte in bytes:
            self._draw(matrix, y-0, byte >> 4)
            self._draw(matrix, y-1, byte & 15)
            y -= 2

class Art:

    def __init__(self, matrix):
        self.paddley = [4, 10]
        self.paddlex = [0, matrix.width()-1]
        self._restart()

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)

    def _restart(self):
        self.scores = [ Score(3, 10, rgb["red4"]), Score(9, 10, rgb["red4"]) ]
        self._serve(random()-0.5)

    def _serve(self, direction):
        self.x = randrange(5, 12)
        self.y = randrange(5, 12)
        self.h = copysign(1, direction)
        self.v = randrange(1, 2)

    def _intersect(self, newx, newy, id):
        if self.paddlex[id] == newx:
            delta = self.paddley[id] - newy
            if abs(delta) < 3:
                return delta

        return None

    def _intersects(self, newx, newy):
        for paddle in range(2):
            accel = self._intersect(newx, newy, paddle)
            if accel is not None:
                return accel

        return None

    def _drawNet(self, matrix):
        for y in range(matrix.width()):
            if ((1+y)/2) % 2 == 0:
                matrix.drawLine(7, y, 8, y, rgb["gray30"])

    def _drawScore(self, matrix):
        for score in self.scores:
            score.display(matrix)

    def _updateBat(self, matrix, id):
        if random() > .7:
            self.paddley[id] = min(matrix.height()-2, max(2, int(self.paddley[id] + self.v)))

        matrix.drawLine(self.paddlex[id], self.paddley[id]-2, self.paddlex[id], self.paddley[id]+2, rgb["yellow"])

    def _drawBats(self, matrix):
        for paddle in range(2):
            self._updateBat(matrix, paddle)
  
    def _drawBall(self, matrix):
        matrix.drawPixel(self.x, self.y, rgb["white"])
        newx, newy = (self.x + self.h, self.y + self.v)

        accel = self._intersects(newx, newy)
        if accel is not None:
            self.h = -self.h
            self.v = accel
        elif newx<0 or newx>=matrix.width():
            if self.scores[0].bump():
                self._restart()

            self._serve(self.h)
        else:
            self.x = newx

        if newy<0 or newy>=matrix.height():
            self.v = -self.v
        else:
            self.y = newy

    def refresh(self, matrix):
        matrix.clear()

        self._drawNet(matrix)
        self._drawScore(matrix)
        self._drawBats(matrix)
        self._drawBall(matrix)

    def interval(self):
        return 200

