from ..drivers import driver
from functools import reduce
import operator
import numpy as np

from ..colors import BLACK
from ..nphue import rgb_to_hsv, hsv_to_rgb

from ..buffer import OPCBuffer

from ..utils.prof import timefunc
from ..utils.wrapexception import wrapexception

DTYPE = np.uint8


import logging
logger = logging.getLogger(__name__)

from .cursor import Cursor
from .filter import Filter
from .hq import HQ
from .pixel import Pixel
from .plot import Plot
from .transform import Transform


class OPCMatrix(Cursor, Filter, HQ, Pixel, Plot, Transform):

    """
    This is the main class for interacting with a display. Generally
    speaking, most of what  you need to operate on a display is accessible
    through the matrix api.

    Implementation-wise, the address you provide in the constructor
    will determine which hardware driver is invoked.

    check out the other classes in this module for more information, and see
    the provided examples for usage.
    """

    HQMULT = 4

    @timefunc
    def __init__(self, width, height, address, zigzag=False, flipud=False,
                 fliplr=False, debug=False):
        """
        width -- renderable width
        height -- renderable height
        address -- display type, or OPC address. Type is ansi, raw, or None
        zigzag -- set to true if alternate rows travel opposite directions
        flipud -- top is bottom
        fliplr -- left is right
        """

        self.width = width
        self.height = height
        self.zigzag = zigzag
        self.flipud = flipud
        self.fliplr = fliplr

        self.debug = debug

        self.buf_std = OPCBuffer(width, height)
        if address is None:
            # matrix instances without an address are used as intermediate
            # buffers by various arts
            self.client = None
            self.buf_hq = self.buf_std
            self.internal = True
        else:
            module = driver(address)
            self.client = module.Driver(width, height, address)
            # only "real" displays get a high quality option
            self.buf_hq = OPCBuffer(width*self.HQMULT, height*self.HQMULT)
            self.internal = False

        self.hq(False)
        self.setCursor()

    @timefunc
    def terminate(self):
        self.client.terminate()

    @timefunc
    def clone(self):
        """Return a copy of the matrix as a new matrix
        """
        copy = OPCMatrix(
                self.width, self.height, 
                address=None,
                zigzag=self.zigzag, flipud=self.flipud, fliplr=self.fliplr
                )

        if self.ishq:
            copy.hq()

        return copy

    @timefunc
    def hq(self, ishq=True):
        """Switches HQ (supersampling) mode on or off. Clears the
        display on switch-on"""
        if ishq and not self.internal:
            self.ishq = ishq
            self.buf = self.buf_hq
            self.clear()
        else:
            self.ishq = False
            self.buf = self.buf_std

        self.width = self.buf.width
        self.height = self.buf.height
        self.numpix = self.width * self.height
        self.smallest = min(self.height, self.width)
        self.midWidth = self.width / 2.0
        self.midHeight = self.height / 2.0

    @timefunc
    def setFirmwareConfig(self, nodither=False, nointerp=False,
                          manualled=False, ledonoff=True):

        if self.client is not None:
            self.client.setFirmwareConfig(nodither, nointerp, manualled, ledonoff)

    @timefunc
    def setBrightness(self, gamma, bright):
        self.client.setGlobalColorCorrection(gamma, bright, bright, bright)

    @timefunc
    def setGlobalColorCorrection(self, gamma=2.5, r=0.6, g=0.6, b=0.6):
        self.client.setGlobalColorCorrection(gamma, r, g, b)

    @timefunc
    def copyBuffer(self, buf):
        self.buf.copyImage(buf)

    @timefunc
    def copy(self, source, x=None, y=None):
        """
        XXX: This assumes that the source matrix is larger than the
        destination.

        Copy one matrix to another. The default behavior is to scale
        down the source matrix to fit the target matrix.

        Alternatively, supplying x and y will render the source matrix
        from the given (x, y) to fill the target.
        """
        if x is None and y is None:
            self.buf.scaledCopy(source.buf)
        else:
            self.buf.panCopy(source.buf, x, y)

    def _clipx(self, x):
        return int(max(min(x, self.width-1), 0))

    def _clipy(self, y):
        return int(max(min(y, self.height-1), 0))

    @timefunc
    def _clip(self, x, y):
        return (self._clipx(x), self._clipy(y))

    @timefunc
    def show(self, channel=0):
        """
        Write the buf to the display device. If the hq buffer
        is enabled, then down-sample to the standard buffer
        first.
        """
        buf = self.buf_std

        if self.ishq:
            buf.scaledCopy(self.buf_hq)

        if self.zigzag or self.flipud or self.fliplr:
            pixels = np.copy(buf.buf)
            if self.zigzag:
                pixels[0::2] = pixels[0::2, ::-1]
            if self.flipud:
                pixels = np.flipud(pixels)
            if self.fliplr:
                pixels = np.fliplr(pixels)
        else:
            pixels = buf.buf

        return self.client.putPixels(channel, pixels)
