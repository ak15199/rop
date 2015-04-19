from opc.colormap import Colormap
from opc.colors import BLACK, BLUE, YELLOW, RED, GREEN

from baseclasses.diamondsquare import DiamondSquare


class Art(DiamondSquare):

    description = "Thin plasma using DiamondSquare and colormap rotation"

    def __init__(self, matrix):
        super(Art, self).__init__(matrix, self.generate, maxticks=20,
                                  interpolate=False)

        self.colormap = Colormap(130)
        self.colormap.flat(0, 130, BLACK)

        self.colormap.flat(20, 30, BLUE)
        self.colormap.flat(50, 60, YELLOW)
        self.colormap.flat(80, 90, RED)
        self.colormap.flat(110, 120, GREEN)

        self.colormap.blur()

        self.diamond.generate()

    def generate(self, matrix, diamond):
        self.colormap.rotate()
        self.diamond.translate(matrix, colormap=self.colormap)
