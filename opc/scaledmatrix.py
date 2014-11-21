from matrix import OPCMatrix


class ScaledMatrix(OPCMatrix):

    """
    abstract matrix scaling. Use the constructor to build a backing buffer to
    draw on, then call scaleDown to copy over to the basematrix
    """

    def __init__(self, basematrix, scale=4):
        self.scale = scale
        self.basematrix = basematrix
        super(ScaledMatrix, self).__init__(scale*basematrix.width, scale*basematrix.height, None, True)

    def scaleDown(self):
        self.basematrix.copy(self)
