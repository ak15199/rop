from math import sin, cos, pi
from random import random

from opc.colors import RED, GREEN, BLUE, BLACK
from opc.hue import getColorGen
from opc.matrix import OPCMatrix, HQ

import numpy as np

import Image


class Art(object):

    description = "RGB variable frequency sine waves"

    def __init__(self, matrix):
        pass

    def start(self, matrix):
        matrix.clear()

    def refresh(self, matrix):
        matrix.drawImage("lena.jpg")
        #self.lena = Image.open("lena.jpg").rotate(-90, Image.BICUBIC).resize((matrix.width, matrix.height), Image.ANTIALIAS)
        #matrix.buf.buf = np.asarray(self.lena)
        #matrix.buf.buf.setflags(write=True)

    def interval(self):
        return 150
