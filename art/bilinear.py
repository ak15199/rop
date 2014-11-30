from basecls.bilinear import Bilinear


class Art(Bilinear):

    description = "Bilinear interpolation between four random hues"

    def __init__(self, matrix):
        super(Art, self).__init__(matrix)
