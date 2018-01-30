from _baseclass import ArtBaseClass

from math import sqrt
from random import random

from opc.hue import getColorGen

SCALE = 4


class Art(ArtBaseClass):

    description = "Demo image rotation"

    def __init__(self, matrix, config):
        self.hue = getColorGen(0.006)

    def start(self, matrix):
        matrix.hq(True)

    def refresh(self, matrix):
        color = self.hue.next()
        width = matrix.smallest*0.45
        hole  = matrix.smallest*0.25

        mw = matrix.midWidth
        mh = matrix.midHeight
        
        a = (mw, mh+width)
        b = (mw+width, mh)
        c = (mw, mh-width)
        d = (mw-width, mh)
        e = (mw, mh+hole)
        f = (mw+hole, mh)
        g = (mw, mh-hole)
        h = (mw-hole, mh)

        matrix.shift(dh=0.95)

        matrix.fillPoly([a, e, f, b], color)
        matrix.fillPoly([b, f, g, c], color)
        matrix.fillPoly([c, g, h, d], color)
        matrix.fillPoly([d, h, e, a], color)

        matrix.rotate(5)

    def interval(self):
        return 80
