from .baseclasses.blobs import Blobs

from ._baseclass import ArtBaseClass

class Art(Blobs):
#class Art(ArtBaseClass):

    description = "Bouncing blobs (psychedelic mix)"

    def start(self, matrix):
        pass

    def refresh(self, matrix):

        #matrix.fillCircle( 10, 7, 5, (255, 255, 255))

        matrix.fade(0.97)
        matrix.rotate(5)
        for pen in self.pens:
            pen.clock(matrix)
