from opc.matrix import OPCMatrix
from opc.colormap import Colormap
from opc.colors import *
from opc.matrix import OPCMatrix

from basecls.diamondsquare import DiamondSquare

class Art(DiamondSquare):

    description = "Thin plasma using DiamondSquare and colormap rotation"

    def __init__(self, matrix):
        super(Art, self).__init__(matrix, self.generate, maxticks=20,
                interpolate=False)

        self.colormap = Colormap(130)
        self.colormap.flat(  0,  120, BLACK)

        self.colormap.flat( 20,  25,  BLUE)
        self.colormap.flat( 50,  55,  YELLOW)
        self.colormap.flat( 80,  85,  RED)
        self.colormap.flat(110, 115,  GREEN)

        self.colormap.soften()

        self.diamond.generate()

    def generate(self, matrix, diamond):
        self.colormap.rotate()
        self.diamond.translate(matrix, colormap=self.colormap)
        matrix.soften(0.5)
