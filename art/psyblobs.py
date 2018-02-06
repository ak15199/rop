from .baseclasses.blobs import Blobs


class Art(Blobs):

    description = "Bouncing blobs (psychedelic mix)"

    def refresh(self, matrix):
        matrix.fade(0.97)
        matrix.rotate(5)
        for pen in self.pens:
            pen.clock(matrix)
