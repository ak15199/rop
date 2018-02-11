from .. _baseclass import ArtBaseClass

from opc.hue import getHueGen


SEGMENTS=4
HUEDELTA=1/(SEGMENTS*1.5)


class Barber(ArtBaseClass):

    def __init__(self, matrix, config):
        self.width = int(matrix.width/SEGMENTS)
        self.hue = getHueGen(step=0.01)

    def start(self, matrix):
        pass

    def _line(self, matrix, x1, x2, hue):
        raise NotImplementedError

    def refresh(self, matrix):
        matrix.scroll("up")
        matrix.scroll("right")

        hue = next(self.hue)
        for segment in range(SEGMENTS):
            self._line(
                    matrix,
                    self.width*segment,
                    self.width*(segment+1),
                    hue+(HUEDELTA*segment)
                    )

    def interval(self):
        return 120
