from ._baseclass import ArtBaseClass

from opc.matrix import HQ
from random import random
import numpy as np


class Channel(object):

    def __init__(self, matrix):
        ones = np.ones(matrix.numpix).reshape((matrix.height, matrix.width))
        self.x = ones*np.arange(matrix.width)
        self.y = np.flipud(np.rot90(np.rot90(ones)*np.arange(matrix.height)))

        self.delta = random()*0.5+0.2 

    def refresh(self, matrix):
        self.x += self.delta
        self.y += self.delta

        c1 = self.x/16
        c2 = self.y/8
        c3 = (self.x+self.y)/16
        c4 = np.sqrt((self.x*self.x)+(self.y*self.y))/8

        channel = np.sum(np.sin(c) for c in (c1, c2, c3, c4))
        return np.fmod(np.fabs(1+channel/2), 1.0)


class Art(ArtBaseClass):

    description = "Plasma by RGB channel"

    def __init__(self, matrix, config):
        with HQ(matrix):
            self.channels = [Channel(matrix) for channel in range(3)]

    def start(self, matrix):
        matrix.hq()

    def refresh(self, matrix):

        channels = [255*channel.refresh(matrix) for channel in self.channels]

        for y in range(matrix.height):
            for x in range(matrix.width):
                matrix.drawPixel(x, y, (
                    channels[0][y, x],
                    channels[1][y, x],
                    channels[2][y, x],
                    ))

    def interval(self):
        return 270
