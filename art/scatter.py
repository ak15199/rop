from opc.hue import hsvToRgb
from opc.matrix import OPCMatrix

from random import random
from utils.lfsr import lfsr256

class Art:

    description = "Use a 256 bit LFSR to 'randomly' fill the display"

    def __init__(self, matrix):
        pass

    def start(self, matrix):
        self.random = lfsr256()
        self.hue = random()
        matrix.clear()

    def refresh(self, matrix):
        try:
            pos = self.random.next()
        except:
            self.random = lfsr256()
            self.hue = random()
            pos = self.random.next()
            
        color = hsvToRgb(self.hue, 1, random())
        matrix.setStripPixel(pos, color)
  
    def interval(self):
        return 50

