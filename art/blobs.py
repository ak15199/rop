from .baseclasses.blobs import Blobs


class Art(Blobs):

    description = "Bouncing blobs (basic edition)"

    def refresh(self, matrix):
        matrix.clear()

        for pen in self.pens:
            pen.clock(matrix)
