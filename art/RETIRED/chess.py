from ._baseclass import ArtBaseClass

from opc.hue import getHueGen, hsvToRgb

from math import sqrt

GRIDSIZE = 8

C_BACKGROUND = (96, 64, 24)
C_BORDER = (128, 128, 128)


class Art(ArtBaseClass):

    description = "A silly chess board"

    def __init__(self, matrix, config):
        self.hue = getHueGen(0.0005)

    def start(self, matrix):
        matrix.clear(C_BACKGROUND)

    def refresh(self, matrix):
        hue = next(self.hue)

        # pixels per squre 
        pps = int((sqrt(matrix.numpix)-1)/GRIDSIZE)

        xcorner = matrix.midWidth - pps*(GRIDSIZE/2)
        ycorner = matrix.midHeight - pps*(GRIDSIZE/2)

        matrix.drawRect(xcorner-1, ycorner-1,
                        pps*GRIDSIZE+1, pps*GRIDSIZE+1, C_BORDER)

        for x in range(GRIDSIZE):
            for y in range(GRIDSIZE):
                black = (x & 1) ^ (y & 1)
                if black:
                    color = hsvToRgb(hue, s=0.7, v=0.5)
                else:
                    color = hsvToRgb(hue + 0.2, v=0.8)

                matrix.fillRect(xcorner+pps*x, ycorner+pps*y, pps, pps, color)


    def interval(self):
        return 100
