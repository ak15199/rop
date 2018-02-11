from ._baseclass import ArtBaseClass

from random import randint, random

from opc.colors import BLACK
from opc.hue import getColorGen


class Instance(object):

    def __init__(self, matrix, x, color):
        self.color = color
        self.mid = matrix.height/2
        self.x = x
        self.y = 0

    def vote(self, value):
        if self.x == value:
            return True

        if self.y > self.mid:
            return False

        if self.x-1 <= value <= self.x+1:
            return True

        return False

    def next(self, matrix):
        matrix.drawPixel(self.x, self.y, self.color)

        self.y += 1
        return self.y < matrix.height


class Art(ArtBaseClass):

    description = "Pixels floating upwards with a trail"

    def __init__(self, matrix, config):
        self.count = matrix.width/3
        self.color = getColorGen(step=0.015, hue=random())
        self.y = matrix.height

    def start(self, matrix):
        self.instances = []

    def _vote(self, matrix):
        while True:
            value = randint(0, matrix.width-1)
            if any([instance.vote(value) for instance in self.instances]):
                continue

            return value
        
    def refresh(self, matrix):
        matrix.fade(0.95)
        matrix.maskbelow(55, BLACK)

        if len(self.instances)<self.count and random()<0.6:
            new = self._vote(matrix)
            self.instances.append(Instance(matrix, new, next(self.color)))

        self.instances = [instance for instance in self.instances if instance.next(matrix)]

    def interval(self):
        return 80
