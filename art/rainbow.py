from opc.matrix import OPCMatrix
from opc.hue import hsvToRgb

class Art(object):

    description = "Slow transition of hues across the display"

    def __init__(self, matrix):
        self.base = 0;

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        self.base += 1
        for x in range(matrix.width):
            hue = ((self.base+32*x) % 1024)/1024.0
            for y in range(matrix.height):
                pcent50 = 0.50*float(y)/(matrix.height-1)
                sat = .5 + pcent50
                val = 1 - pcent50
                matrix.drawPixel(x, y, hsvToRgb(hue, sat, val))
  
    def interval(self):
        return 100

