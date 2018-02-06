from ._baseclass import ArtBaseClass

from opc.hue import hsvToRgb

from random import random, randrange


class Rectangle(object):

    def __init__(self, matrix):
        self.value = 0.0
        self.hue = random()

        self.x = randrange(0, matrix.width)
        self.y = randrange(0, matrix.height)
        self.w = randrange(matrix.width/8, matrix.width/2)
        self.h = randrange(matrix.height/8, matrix.height/2)

    def update(self, matrix):
        self.value += 0.2

        matrix.fillRect(
            self.x, self.y,
            self.w, self.h,
            hsvToRgb(h=self.hue, v=self.value),
            )

        return self.value < 1


class Art(ArtBaseClass):

    description = "Random colored rectangles that fade with time"

    def __init__(self, matrix, config):
        self.rect = Rectangle(matrix)

    def start(self, matrix):
        matrix.clear()

    def refresh(self, matrix):
        matrix.fade(0.95)

        if not self.rect.update(matrix):
            self.rect = Rectangle(matrix)

    def interval(self):
        return 200
