from opc.colors import *
from opc.matrix import OPCMatrix

from random import randrange

DIAMETER = 8

class Art:

    def __init__(self, matrix):
        self.scale = 4
        self.matrix = OPCMatrix(self.scale*matrix.width(), self.scale*matrix.height(), None, True)
        self.x = 0
        self.y = self.matrix.height()
        self.dx = 1
        self.dy = -1.4

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)
        matrix.clear()

    def _ball(self, matrix, color):
        self.matrix.fillRect(self.x, self.y, DIAMETER, DIAMETER, color)

    def refresh(self, matrix):
        self._ball(matrix, BLACK)

        self.x = self.x + self.dx
        self.y = self.y + self.dy

        if self.x < 0 or self.x >= (self.matrix.width()-DIAMETER):
            self.dx = -self.dx

        if self.y < 0 or self.y >= self.matrix.height():
            self.y = min(max(self.y, 0), (self.matrix.height()-DIAMETER))
            self.dy = -self.dy

        accel = 1.2
        if self.dy < 1:
            self.dy = self.dy * accel
        else:
            self.dy = self.dy / accel
        
        self._ball(matrix, RED)
        matrix.copy(self.matrix)
  
    def interval(self):
        return 200

