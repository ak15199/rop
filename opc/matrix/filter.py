import numpy as np

from ..nphue import rgb_to_hsv, hsv_to_rgb

from ..utils.prof import timefunc


DTYPE = np.uint8


class Filter(object):

    @timefunc
    def maskbelow(self, thresh, color):
        """
        Set (r, g, b) values below an average value of thresh
        to value
        """
        keys = np.mean(self.buf.buf,2)<thresh
        self.buf.buf[keys] = color

    @timefunc
    def maskabove(self, thresh, color):
        """
        Set (r, g, b) values above an average value of thresh
        to value
        """
        keys = self.buf.buf[np.mean(self.buf.buf,2)>thresh]
        self.buf.buf[keys] = color

    @timefunc
    def shift(self, dh=1.0, ds=1.0, dv=1.0):
        """
        Shift any of hue, saturation, and value on the matrix, specifying
        the attributes that you'd like to adjust
        """
        hsv = rgb_to_hsv(self.buf.buf)
        mod = hsv * np.array([dh, ds, dv])
        rgb = hsv_to_rgb(mod)

        self.buf.buf = rgb

    @timefunc
    def fade(self, divisor):
        """
        Special case of shift for just value that'll be faster than doing it
        the long way.
        """
        buf = self.buf.buf * divisor
        self.buf.buf = buf.astype(dtype=DTYPE)

    def blur(self, radius=3):
        """Soften influence pixel color from our neighbors"""
        self.buf.blur(radius)

    def mask(self, mask):
        """Perform bit-wise mask on the buffer"""
        self.buf.mask(mask.buf)
