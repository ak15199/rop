from baseclasses.bilinear import Bilinear


class Art(Bilinear):

    description = "Downsampled bilinear interpolation"

    def __init__(self, matrix, config):
        super(Art, self).__init__(matrix, config)

        self.bits = 192
