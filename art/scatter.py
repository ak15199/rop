from opc.hue import hsvToRgb
from opc.matrix import OPCMatrix

from random import random
from utils.lfsr import lfsr

class Art:

    def __init__(self, matrix):
        pass

    def start(self, matrix):
        self.random = lfsr()
        self.hue = random()
        matrix.clear()

    def refresh(self, matrix):
        try:
            pos = self.random.next()
        except:
            self.random = lfsr()
            self.hue = random()
            pos = self.random.next()
            
        color = hsvToRgb(self.hue, 1, random())
        matrix.setStripPixel(pos, color)
  
    def interval(self):
        return 50

