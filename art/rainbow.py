from opc.matrix import OPCMatrix
from opc.hue import hsvToRgb

class Art:

    def __init__(self, matrix):
        self.base = 0;

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        self.base += 1
        for x in range(0, matrix.width()):
            hue = ((self.base+32*x) % 1024)/1024.0
            matrix.drawLine(x, 0, x, matrix.height(), hsvToRgb(hue))
  
    def interval(self):
        return 200

