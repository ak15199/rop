from .baseclasses.barber import Barber

from opc.hue import hsvToRgb


class Art(Barber):

    description = "Barber-pole-esque (clean)"

    def _line(self, matrix, x1, x2, hue):
        color = hsvToRgb(hue, 1, 1)
        matrix.drawLine( x1, 0, x2, 0, color)
