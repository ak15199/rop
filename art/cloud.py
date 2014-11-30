from basecls.diamondsquare import DiamondSquare


class Art(DiamondSquare):

    description = "Clouds drawn with the diamond square algorithm"

    def __init__(self, matrix):
        super(Art, self).__init__(matrix, self.generate)
        self.hue = 0.1

    def generate(self, matrix, diamond):
        diamond.generate()
        diamond.translate(matrix, hue=self.hue)
