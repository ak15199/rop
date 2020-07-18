import numpy as np

from ..utils.prof import timefunc
from ..utils.wrapexception import wrapexception

import logging
logger = logging.getLogger(__name__)


class Pixel(object):

    @timefunc
    def setStripPixel(self, z, color):
        """
        Exposed helper method that sets a given pixel in the unrolled strip
        of LEDs.
        """
        x = int(z / self.height)
        y = int(z % self.height)

        self.buf.buf[x, y] = color

    @timefunc
    def getPixel(self, x, y, wrap=False):
        """
        Retrieve the color tuple of the pixel from the specified location
        """
        if wrap:
            x = x % self.width
            y = y % self.height

        return self.buf.buf[x, y]

    @timefunc
    @wrapexception(logger)
    def drawPixel(self, x, y, color, alpha=None):
        """
        Set the pixel tuple at the specified location.  Perform no operation
        if the color value is None, or the address out of bounds
        """
        x, y = int(x), int(y)

        if alpha is None:
            self.buf.buf[x, y] = color
        else:
            a0 = alpha
            a1 = 1-alpha
            self.buf.buf[x, y] = np.asarray(color)*a0 + self.buf.buf[x, y]*a1

    @timefunc
    @wrapexception(logger)
    def drawPixels(self, coords, color, alpha=None):
        """
        Set the pixel tuple at the set of specified locations.  Like drawPixel,
        but operates over a list of (x, y) coordinates.
        """
        coords = [(coord[0], coord[1]) for coord in coords if
                  coord[0] >= 0 and coord[0] < self.width and
                  coord[1] >= 0 and coord[1] < self.height]

        if not coords:  # when everything is off screen
            return

        xs, ys = zip(*coords)

        if alpha is None:
            self.buf.buf[xs, ys] = color
        else:
            a0 = alpha
            a1 = 1-alpha
            self.buf.buf[xs, ys] = (np.asarray(color)*a0 +
                                    self.buf.buf[xs, ys]*a1)
