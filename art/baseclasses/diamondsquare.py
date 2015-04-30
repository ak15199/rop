from .. _baseclass import ArtBaseClass

from opc.matrix import OPCMatrix

from art.utils.diamondsquare import DiamondSquareAlgorithm

DFLTTICKS = 350


class DiamondSquare(ArtBaseClass):

    def __init__(self, matrix, generate, maxticks=DFLTTICKS, interpolate=True):
        self.diamond = DiamondSquareAlgorithm(matrix.width, matrix.height)
        self.matrix = OPCMatrix(matrix.width, matrix.height, None)

        self.generate = generate
        self.ticks = 0
        self.maxticks = maxticks
        self.interpolate = interpolate

    def start(self, matrix):
        matrix.clear()

    def refresh(self, matrix):
        # ticks allow us to keep track of how much time has passed
        # since the last generation. This gives us opportunity for
        # both a smooth transition, and time to observe the result
        if self.ticks <= 0:
            self.generate(self.matrix, self.diamond)
            self.ticks = self.maxticks

        self.ticks -= 10

        if self.interpolate:
            matrix.buf.avg(self.matrix.buf, 0.9)
        else:
            matrix.copy(self.matrix, 0, 0)

    def interval(self):
        return 50
