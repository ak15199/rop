from opc.matrix import OPCMatrix
from opc.hue import hsvToRgb

from random import randrange

# XXX: This one is a work in progress and doesn't work super well yet :)

class Art:

    def __init__(self, matrix):
        pass

    def start(self, matrix):
        pass

    def _point(self, x, y, max):
        n=0
        u=x
        v=y
        
        while True:
            a = u*u
            b = v*v
            if a+b >= 4:
                return n

            n += 1
            if n == max:
                return None

            a = a-b+x
            v = 2*u*v+y
            u = a


    def refresh(self, matrix):
        for x in range(matrix.width()):
            for y in range(matrix.height()):
                point = self._point(x/6-1, y/6-1, 15)
                if point is not None:
                    hue = point/20.0
                    matrix.drawPixel(x, y, hsvToRgb(hue))
        pass
  
    def interval(self):
        return 400

