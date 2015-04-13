import numpy as np
from scipy.ndimage import interpolation
from scipy import signal

from colors import BLACK
from utils.prof import timefunc

import logging

DTYPE = np.uint8


class OPCBuffer(object):
    """
    Provdes primitive buffer-level storage and operations.

    OPCBuffer is usually considered an internal class. But it
    comes in handy (e.g.) if you want to draw on a larger "virtual"
    array, and scale down for rendering on a physical array.
    """

    @timefunc
    def __init__(self, width, height, color=BLACK):
        self.width = width
        self.height = height
        self.shape = (width, height, 3)
        self.buf = np.empty(shape=self.shape, dtype=DTYPE)
        self.clear(color)

    def _sameSize(self, other):
        return self.buf.shape == other.buf.shape

    def __len__(self):
        return len(self.buf)

    def __add___(self, other):
        pass

    def __or___(self, other):
        pass

    def __xor___(self, other):
        pass

    def __and___(self, other):
        pass

    @timefunc
    def reds(self):
        """ get all of the reds from the buffer """
        return self.buf[:, :, 0]

    @timefunc
    def greens(self):
        """ get all of the greens from the buffer """
        return self.buf[:, :, 1]

    @timefunc
    def blues(self):
        """ get all of the blues from the buffer """
        return self.buf[:, :, 2]

    @timefunc
    def avg(self, other, weight=.5):
        """ Get a weighted average of two buffers.  """
        if not self._sameSize(other):
            raise InvalidArgument("Matrices are different sizes")

        if weight < 0.0 or weight > 1.0:
            raise InvalidArgument("Invalid Weight")

        buf1 = (self.buf * weight)
        buf2 = (other.buf * (1.0-weight))
        self.buf = buf1.astype(dtype=DTYPE) + buf2.astype(dtype=DTYPE)

    @timefunc
    def clear(self, color=BLACK):
        self.buf[:][:] = color

    @timefunc
    def downSample(self, bits):
        self.buf &= bits

    @timefunc
    def panCopy(self, source, ox, oy):
        """Blit from the source buf to the destination"""
        xend = ox+self.width
        yend = oy+self.height
        try: # happy path
            self.buf[:][:] = source.buf[ox:xend, oy:yend]
        except ValueError:
            xbig = xend > source.width
            ybig = yend > source.height
            xgap = xend - source.width
            ygap = yend - source.height
            window = source.buf[ox:(xend-xgap), oy:(yend-ygap)]

            if xbig:
                if ybig:
                    # XX | @
                    # XX | @
                    # -- | -
                    # oo | @
                    window = source.buf[ox:(xend-xgap), oy:(yend-ygap)]
                    window = np.concatenate((window, source.buf[0:xgap, oy:yend]), axis=0)
                    window = np.concatenate((window, window[:, 0:xgap]), axis=1)
                else:
                    # XXX
                    # XXX
                    # ---
                    # ooo
                    window = source.buf[ox:(xend-xgap), oy:yend]
                    window = np.concatenate((window, source.buf[0:xgap, oy:yend]), axis=0)
            elif ybig:
                    # XX | o
                    # XX | o
                    # XX | o
                    window = source.buf[ox:xend, oy:(yend-ygap)]
                    window = np.concatenate((window, source.buf[ox:xend, 0:ygap]), axis=1)

            self.buf[:][:] = window

    @timefunc
    def scaledCopy(self, source):
        """
        Reduce the size of the source buffer to fit the destination buffer.

        Process each gun independently. For each gun, we need to reshape
        its array so as to line up all of the values associated with the
        superpixel in a single row. This allws us to perform a mean
        operation on the array, essentially building the new buffer

        For the array a=np.arange(4*4*3).reshape((4,4,3)), reds will
        consist of:

              array([[ 0,  3,  6,  9],
                     [12, 15, 18, 21],
                     [24, 27, 30, 33],
                     [36, 39, 42, 45]])

        If we're going from 4x4 to 2x2, then the reduction ratio is 2,
        meaning that we will take four values from the superpixel to
        calculate the new value.  In this case, the top LH pixel will be
        the average of (0, 3, 12, 15).
        """

        ratio = source.width / self.width
        if ratio < 1:  # Can't zoom up
            # XXX: This should throw
            return

        guns = []
        r, g, b = source.reds(), source.greens(), source.blues()
        for gun in (r, g, b):
            new = np.average(np.split(np.average(np.split(gun, source.width //
                             ratio, axis=1), axis=-1),
                             source.height // ratio, axis=1),
                             axis=-1)
            guns.append(new)

        self.buf = np.dstack(guns).reshape((self.width, self.height, 3))

    @timefunc
    def rotate(self, angle):
        self.buf = interpolation.rotate(self.buf, angle, reshape=False,
                output=DTYPE)

    @timefunc
    def _convolve(self, kernel):
        guns = []
        scale = np.sum(kernel)*256
        r, g, b = self.reds(), self.greens(), self.blues()
        for gun in (r, g, b):
            new = signal.convolve2d(gun/scale, kernel, mode="same",
            boundary="symm")
            guns.append(new*255)

        self.buf = np.dstack(guns).reshape((self.width, self.height, 3))

    @timefunc
    def blur(self):
        gaussian = np.array([
            [1, 2, 1],
            [2, 4, 2],
            [1, 2, 1],
            ], dtype=np.float32)

        self._convolve(gaussian)
        logging.info(str(self.buf))
