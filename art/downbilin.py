from basecls.bilinear import Bilinear

class Art(Bilinear):

    description = "Downsampled bilinear interpolation"

    def __init__(self, matrix):
        super(Art, self).__init__(matrix, 192)
