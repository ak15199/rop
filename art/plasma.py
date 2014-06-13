from opc.matrix import OPCMatrix
from opc.hue import hsvToRgb
import time
from math import sin, sqrt, fabs, fmod
import dpyinfo

class Art:

    def __init__(self, matrix):
        self.base=128000

    def start(self, matrix):
        pass

    def _dist(self, a,b,c,d):
        return sqrt((c-a)*(c-a)+(d-b)*(d-b))

    def refresh(self, matrix):
        minval, maxval = (10, -10)

        for y in range(matrix.height()):
            for x in range(matrix.width()):
                hue = (
                    sin(self._dist(x + self.base, y, 128.0, 128.0) / 8.0)
                  + sin(self._dist(y, y, 64.0, 64.0) / 8.0)
                  + sin(self._dist(x, y + self.base / 7, 192.0, 64) / 7.0)
                  + sin(self._dist(y, x, 192.0, 100.0) / 8.0))
           
                hue = fmod(fabs(1+hue/2), 1.0)
                matrix.drawPixel(x, y, hsvToRgb(hue))
        
        self.base+=0.1
  
    def interval(self):
        return 100

