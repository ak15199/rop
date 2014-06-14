from opc.matrix import OPCMatrix
from opc.hue import hsvToRgb
from math import sin, cos

from random import randrange

# XXX: This one is a work in progress and doesn't work super well yet :)

class Art:

    def __init__(self, matrix):
        scale = 4
        self.matrix = OPCMatrix(scale*matrix.width(), scale*matrix.height(), None, False)

    def start(self, matrix):
        max = 30
        self.angle = 0
        for x in range(self.matrix.width()):
            for y in range(self.matrix.height()):
                px = (2.0 * x)/self.matrix.width()-1
                py = (2.0 * y)/self.matrix.height()-1
                point = self._point(px, py, max)
                if point is not None:
                    hue = (0.0+point)/max
                    self.matrix.drawPixel(x, y, hsvToRgb(hue))

    def _point(self, x, y, max):
        n=0
        u=x
        v=y
        
        while True:
            a = u*u
            b = v*v
            if a+b >= 4:
                #print x, y, n
                return n

            n += 1
            if n == max:
                return None

            a = a-b+x
            v = 2*u*v+y
            u = a


    def refresh(self, matrix):
        center = self.matrix.width()/3
        x = center + center*sin(self.angle)
        y = center + center*cos(self.angle)
        matrix.copy(self.matrix, x=x, y=y)

        self.angle += 0.1
  
    def interval(self):
        return 200

