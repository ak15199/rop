from PIL import Image, ImageFilter

import numpy as np

from colors import BLACK
from utils.prof import timefunc

DTYPE = np.uint8


class OPCBuffer(object):
    """
    Provdes primitive buffer-level storage and operations.
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

    def __xor___(self, other):
        pass

    @timefunc
    def mask(self, mask):
        self.buf = self.buf.astype(dtype=DTYPE) & mask.buf.astype(dtype=DTYPE)

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
        try:  # happy path
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
                    window = np.concatenate((window, source.buf[0:xgap,
                                             oy:yend]), axis=0)
                    window = np.concatenate((window, window[:, 0:xgap]),
                                            axis=1)
                else:
                    # XXX
                    # XXX
                    # ---
                    # ooo
                    window = source.buf[ox:(xend-xgap), oy:yend]
                    window = np.concatenate((window, source.buf[0:xgap,
                                             oy:yend]), axis=0)
            elif ybig:
                    # XX | o
                    # XX | o
                    # XX | o
                    window = source.buf[ox:xend, oy:(yend-ygap)]
                    window = np.concatenate((window, source.buf[ox:xend,
                                             0:ygap]), axis=1)

            self.buf[:][:] = window

    @timefunc
    def copyImage(self, image):
        self.buf = np.asarray(image)
        self.buf.setflags(write=True)

    @timefunc
    def scaledCopy(self, source):
        # we transpose (width, height) in the copy, this is deliberate
        # since the dimensions are reversed between Image and the buffer.
        i = Image.fromarray(source.buf.astype(DTYPE))
        self.copyImage(i.resize((self.height, self.width), Image.ANTIALIAS))

    @timefunc
    def rotate(self, angle):
        i = Image.fromarray(self.buf.astype(DTYPE))
        self.copyImage(i.rotate(angle, Image.BICUBIC))

    @timefunc
    def flip(self, ud, lr):
        if not any((ud, lr)):
            raise InvalidArgument("Must specify at least one of ud or lr")

        # yes, these two really do get switched over. It's because we all
        # have a different idea on which dimension is for x.
        if lr:
            self.buf = np.flipud(self.buf)

        if ud:
            self.buf = np.fliplr(self.buf)

    @timefunc
    def paste(self, source, mask):
        mask = mask.buf.astype(dtype=DTYPE)
        source = source.buf.astype(dtype=DTYPE)
        self.buf = (self.buf.astype(dtype=DTYPE) & ~mask) | (source & mask)

    @timefunc
    def add(self, source):
        self.buf = (self.buf.astype(dtype=DTYPE) |
                    source.buf.astype(dtype=DTYPE))

    @timefunc
    def blur(self, radius):
        i = Image.fromarray(self.buf.astype(DTYPE))
        self.copyImage(i.filter(ImageFilter.GaussianBlur(radius)))

    def _scroll_left(self, count):
        a = self.buf[:-1, :].flatten()
        b = self.buf[-1, :].flatten()
        self.buf = np.concatenate((b, a)).reshape((self.width, self.height, 3))

    def _scroll_right(self, count):
        a = self.buf[0, :].flatten()
        b = self.buf[1:, :].flatten()
        self.buf = np.concatenate((b, a)).reshape((self.width, self.height, 3))

    def _scroll_up(self, count):
        raise NotImplementedError

    def _scroll_down(self, count):
        raise NotImplementedError

    @timefunc
    def scroll(self, direction, count=1):
        dispatch = {
            "left": self._scroll_left,
            "right": self._scroll_right,
            "up": self._scroll_up,
            "down": self._scroll_down,
            }

        dispatch[direction](count)
