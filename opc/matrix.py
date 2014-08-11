from copy import deepcopy
import numpy as np
import logging

from colors import BLACK
from hue import rgbToHsv, hsvToRgb

from ansiclient import AnsiClient
from fastopc import FastOPC as OpcClient

import utils.pixelstream as pixelstream
from utils.prof import timefunc


DTYPE = np.uint8

"""
This is loosely based on the Adafruit GFX library, although there
are a ton of differences. Some of the differences are where features
have not yet been implemented through necessity, but will be one day.

Others are additional effects that are here because they seemed
pretty cool. Like setting firmware configs on a connection, or
performing a HSV shift on the array.

check out text.py for additional functions to draw text.
"""
class OPCBuffer:
    """
    OPCBuffer is usually considered an internal class. But it
    comes in handy (e.g.) if you want to draw on a larger "virtual"
    array, and scale down for rendering on a physical array.
    """

    @timefunc
    def __init__(self, width, height, color=BLACK):
        shape = (width, height, 3)
        self.buf = np.empty(shape=shape, dtype=DTYPE)
        self.buf[:][:] = color

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
        """
        get all of the reds from the buffer
        """
        return self.buf[:,:,0]

    @timefunc
    def greens(self):
        """
        get all of the greens from the buffer
        """
        return self.buf[:,:,1]

    @timefunc
    def blues(self):
        """
        get all of the blues from the buffer
        """
        return self.buf[:,:,2]

    @timefunc
    def avg(self, other, weight=.5):
        """
        Get a weighted average of two buffers.

        XXX: This will fail silently if either the arrays are different
            sizes, or if the weight isn't sensible. Should probably
            raise exceptions.
        """
        if not self._sameSize(other):
            return
        if weight<0.0 or weight>1.0:
            return

        buf1 = (self.buf * weight)
        buf2 = (other.buf * (1.0-weight))
        self.buf = buf1.astype(dtype=DTYPE) + buf2.astype(dtype=DTYPE)

    @timefunc
    def downSample(self, bits):
        self.buf &= bits

class OPCMatrix:
    @timefunc
    def __init__(self, width, height, address, zigzag=False, pixelDebug=False):
        self.pixelDebug = pixelDebug
        self.width = width
        self.height = height
        self.numpix = width * height

        self.buf = OPCBuffer(width, height)
        self.setCursor()

        if address is None:
            self.client = None
        elif address[0:4] == 'ansi':
            self.client = AnsiClient(address)
            self.client.setGeometry(width, height)
            self.zigzag = False
        else:
            self.client = OpcClient(address)
            self.zigzag = zigzag

    @timefunc
    def setFirmwareConfig(self, nodither=False, nointerp=False, manualled=False, ledonoff=True):
        if self.client is not None:
            data = chr(nodither | (nointerp << 1) | (manualled << 2) | (ledonoff << 3))
            self.client.sysEx(0x0001, 0x0002, data)

    @timefunc
    def clone(self):
        return deepcopy(self)

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
            self._scaledCopy(source)
        else:
            self._panCopy(source, x, y)

    @timefunc
    def _panCopy(self, source, ox, oy):
        for x in range(self.width):
            for y in range(self.height):
                src = source.getPixel(x + ox, y + oy, wrap=True)
                if src is not None:
                    self.drawPixel(x, y, src)

    @timefunc
    def _scaledCopy(self, source):
        """
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
        if ratio < 1: # Can't zoom up
            return

        guns = []
        for gun in (source.buf.reds(), source.buf.greens(), source.buf.blues()):
            new = np.average(np.split(np.average(np.split(gun, source.width //
                ratio, axis=1), axis=-1), source.height // ratio, axis=1),
                axis=-1)
            guns.append(new)

        self.buf.buf = np.dstack(guns).reshape((self.width, self.height, 3))

    @timefunc
    def setStripPixel(self, z, color):
        """
        Exposed helper method that sets a given pixel in the unrolled strip
        of LEDs.
        """
        x = z / self.width
        y = z % self.width

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
    def drawPixel(self, x, y, color):
        """
        Set the pixel tuple at the specified location.  Perform no operation
        if the color value is None, or the address out of bounds
        """
        if x>=self.width or y>=self.height or x<0 or y<0 or color is None:
            return

        self.buf.buf[x, y] = color

    @timefunc
    def _clip(self, x, y):
        return (
                max(min(x, self.width), 0),
                max(min(y, self.height), 0),
            )

    @staticmethod
    @timefunc
    def _shiftPixel(pixel, dh, ds, dv):
        if np.count_nonzero(pixel) == 0:
            return pixel

        h, s, v = rgbToHsv(pixel[0], pixel[1], pixel[2])
        return hsvToRgb(h*dh, s*ds, v*dv)

    @timefunc
    def shift(self, dh=1.0, ds=1.0, dv=1.0):
        """
        Shift any of hue, saturation, and value on the matrix, specifying
        the attributes that you'd like to adjust
        """
        self.buf.buf = pixelstream.process(self.buf.buf, self._shiftPixel, dh,
                ds, dv)

        #reshaped = self.buf.buf.reshape(self.width*self.height, 3)
        #pixels = [self._shiftPixel(pixel, dh, ds, dv) for pixel in reshaped]
        #self.buf.buf = np.asarray(pixels).reshape(self.width, self.height, 3)

    @timefunc
    def fade(self, divisor):
        """
        Special case of shift for just value that'll be faster than doing it
        the long way.
        """
        buf = self.buf.buf * divisor
        self.buf.buf = buf.astype(dtype=DTYPE)

    @timefunc
    def clear(self, color=BLACK):
        """
        Wipe the matrix to any color, defaulting to black
        """
        self.buf.buf[:][:] = color

    @timefunc
    def show(self, channel=0):
        """
        write the buf to the display device
        """
        if self.zigzag:
            pixels = np.copy(self.buf.buf)
            pixels[0::2] = pixels[0::2,::-1]
        else:
            pixels = self.buf.buf

        self.client.putPixels(channel, pixels)

    @timefunc
    def _line(self, x0, y0, x1=None, y1=None):

        if x1 is None and y1 is None:
            x1, y1 = x0, y0
            x0, y0 = self.getCursor()
            self.setCursor((x1, y1))

        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = x1 - x0
        dy = abs(y1 - y0)
        err = dx / 2

        if y0 < y1:
            ystep = 1
        else:
            ystep = -1

        points = []
        while x0 <= x1:
            if steep:
                points.append((y0, x0))
            else:
                points.append((x0, y0))

            x0 += 1
            err -= dy
            if err < 0:
                y0 += ystep
                err += dx

        return points

    @timefunc
    def setCursor(self, pos=(0, 0)):
        """
        Set the cursor position. This is used by draw relative operations
        """
        x, y = pos
        self.cursor = (x, y)

    @timefunc
    def getCursor(self):
        """
        Get the current cursor position
        """
        return self.cursor

    @timefunc
    def drawLineRelative(self, x1, y1, color):
        """
        Draw a line from the current cursor position to the specified address
        """
        path = self._line(x1, y1)
        for x, y in path:
            self.drawPixel(x, y, color)

    @timefunc
    def drawLine(self, x1, y1, x2, y2, color):
        """
        Draw a line between the specified coordinate pairs
        """
        for x, y in self._line(x1, y1, x2, y2):
            self.drawPixel(x, y, color)

    @timefunc
    def drawPoly(self, points, color):
        """
        Draw a polygon described by the array of coordinates
        """
        origin = points.pop(0)

        self.setCursor(origin)
        for point in points:
            x, y = point
            self.drawLineRelative(x, y, color)

        x, y = origin
        self.drawLineRelative(x, y, color)

    @timefunc
    def fillRect(self, x1, y1, w, h, color):
        """
        Draw a filled rectangle
        """
        x1, y1 = int(x1), int(y1)
        w, h = int(w), int(h)
        x2, y2 = (x1+w-1, y1+h-1)
        x1, y1 = self._clip(x1, y1)
        x2, y2 = self._clip(x2, y2)

        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                self.drawPixel(x, y, color)

    @timefunc
    def drawRect(self, x1, y1, w, h, color):
        """
        Draw a rectangle
        """
        self.drawPoly([
                (x1, y1), (x1+w, y1), (x1+w, y1+h), (x1, y1+h)
            ], color)

    @timefunc
    def _circlePair(self, x1, y1, x2, y2, color, hasFill):
        if hasFill:
            self.drawLine(x1, y1, x2, y2, color)
        else:
            self.drawPixel(x1, y1, color)
            self.drawPixel(x2, y2, color)

    @timefunc
    def _circleHelper(self, x0, y0, radius, color, hasFill):
        """
        See http://en.wikipedia.org/wiki/Midpoint_circle_algorithm
        """
        x = radius
        y = 0
        radiusError = 1-x

        while x >= y:
            self._circlePair(x + x0, y + y0, -x + x0, y + y0, color, hasFill)
            self._circlePair(y + x0, x + y0, -y + x0, x + y0, color, hasFill)
            self._circlePair(-y + x0, -x + y0, y + x0, -x + y0, color, hasFill)
            self._circlePair(-x + x0, -y + y0, x + x0, -y + y0, color, hasFill)

            y += 1
            if radiusError < 0:
                radiusError += 2 * y + 1
            else:
                x -= 1
                radiusError += 2 * (y - x + 1)

    @timefunc
    def drawCircle(self, x, y, radius, color):
        self._circleHelper(x, y, radius, color, False)

    @timefunc
    def fillCircle(self, x, y, radius, color):
        self._circleHelper(x, y, radius, color, True)

    @timefunc
    def terminate(self):
        try:
            self.client.terminate()
        except:
            pass # pass if it's a non-ansi client
