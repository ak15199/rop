from .drivers import driver
from copy import deepcopy
from functools import reduce
import operator
import numpy as np

from .colors import BLACK
from .nphue import rgb_to_hsv, hsv_to_rgb

from .buffer import OPCBuffer

from .utils.prof import timefunc
from .utils.wrapexception import wrapexception

DTYPE = np.uint8


import logging
logger = logging.getLogger(__name__)

class HQ(object):

    """
    use the HQ class to savely wrap art init blocks when you need to
    switch on HQ for set-up purposes. For example:

        from opc.matrix import HQ


        class Art(object):

            def __init__(self, matrix):

                with HQ(matrix):
                    initialization stuff...
    """

    def __init__(self, matrix):
        self.matrix = matrix

    def __enter__(self):
        self.matrix.hq()

    def __exit__(self, type, value, traceback):
        self.matrix.hq(False)


class OPCMatrix(object):

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
    def hq(self, ishq=True):
        """Switches HQ mode on or off. Clears the display on switch-on"""
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

    def rotate(self, angle):
        """Rotate the buffer by the given angle"""
        self.buf.rotate(angle)

    def flip(self, ud=None, lr=None):
        """Flip the buffer in one or both axes"""
        self.buf.flip(ud, lr)

    def mask(self, mask):
        """Perform bit-wise mask on the buffer"""
        self.buf.mask(mask.buf)

    def paste(self, source, mask):
        """Paste the masked part of the source buf into our buf"""
        self.buf.paste(source.buf, mask.buf)

    def add(self, source):
        """Update the matrix with non-black pixels from the source"""
        self.buf.add(source.buf)

    def clear(self, color=BLACK):
        """
        Wipe the matrix to any color, defaulting to black.
        """
        self.buf.clear(color)

    def scroll(self, direction):
        """Scroll the matrix in the given direction (left, right, up, down)"""
        self.buf.scroll(direction)

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

    @timefunc
    def _line(self, x1, y1, x2, y2):
        steep = abs(y2 - y1) > abs(x2 - x1)
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dx = x2 - x1
        dy = abs(y2 - y1)
        err = dx / 2

        if y1 < y2:
            ystep = 1
        else:
            ystep = -1

        points = []
        while x1 <= x2:
            if steep:
                points.append((int(y1), int(x1)))
            else:
                points.append((int(x1), int(y1)))

            x1 += 1
            err -= dy
            if err < 0:
                y1 += ystep
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
    def movesCursor(self, x, y):
        return self.cursor[0] != x or self.cursor[1] != y

    @timefunc
    def getCursor(self):
        """
        Get the current cursor position
        """
        return self.cursor

    @timefunc
    def drawLineRelative(self, x1, y1, color, alpha=None):
        """
        Draw a line from the current cursor position to the specified address
        """
        x1, y1 = int(x1), int(y1)

        x0, y0 = self.getCursor()
        self.drawLine(x0, y0, x1, y1, color, alpha)
        self.setCursor((x1, y1))

    @timefunc
    def drawLine(self, x1, y1, x2, y2, color, alpha=None):
        """
        Draw a line between the specified coordinate pairs. If the line is
        horizontal or vertical, then we can optimize the plotting by calling
        it a one pixel wide rectangle
        """
        x1, y1 = int(x1), int(y1)
        x2, y2 = int(x2), int(y2)

        if x1 == x2 or y1 == y2:
            self.fillRectAbsolute(x1, y1, x2, y2, color)
        else:
            coords = self._line(x1, y1, x2, y2)
            self.drawPixels(coords, color, alpha)

    @timefunc
    def drawPoly(self, points, color, alpha=None):
        """
        Draw a polygon described by the array of coordinates
        """
        origin = points.pop(0)

        self.setCursor(origin)
        for x, y in points:
            self.drawLineRelative(x, y, color, alpha)

        x, y = origin
        self.drawLineRelative(x, y, color, alpha)

    @timefunc
    def fillRectAbsolute(self, x1, y1, x2, y2, color):
        """
        Draw an unrotated filled rectangle
        """
        x1, y1 = self._clip(x1, y1)
        x2, y2 = self._clip(x2, y2)

        if x1 == x2:
            if y1 == y2:
                self.buf.buf[x1, y1] = color
            else:
                self.buf.buf[x1, min(y1, y2):max(y1, y2)+1] = color
        else:
            if y1 == y2:
                self.buf.buf[min(x1, x2):max(x1, x2)+1, y1] = color
            else:
                self.buf.buf[min(x1, x2):max(x1, x2)+1,
                             min(y1, y2):max(y1, y2)+1] = color

    @timefunc
    def fillRect(self, x1, y1, w, h, color):
        """
        Draw an unrotated filled rectangle
        """
        x1, y1 = int(x1), int(y1)
        w, h = int(w), int(h)
        x2, y2 = (x1+w-1, y1+h-1)

        self.fillRectAbsolute(x1, y1, x2, y2, color)

    @timefunc
    def drawRect(self, x1, y1, w, h, color):
        """
        Draw a rotated filled rectangle
        """
        self.drawPoly([
            (x1, y1), (x1+w, y1), (x1+w, y1+h), (x1, y1+h)
            ], color)

    @timefunc
    def _circlePair(self, x1, y1, x2, y2, color, hasFill, alpha=None):
        if hasFill:
            self.fillRectAbsolute(x1, y1, x2, y2, color)
        else:
            self.drawPixels([(x1, y1), (x2, y2)], color, alpha)

    @timefunc
    def _circleHelper(self, x0, y0, radius, color, hasFill, alpha=None):
        """
        See http://en.wikipedia.org/wiki/Midpoint_circle_algorithm
        """
        x = radius
        y = 0
        radiusError = 1-x

        while x >= y:
            self._circlePair(x + x0, y + y0, -x + x0, y + y0, color, hasFill,
                             alpha)
            self._circlePair(y + x0, x + y0, -y + x0, x + y0, color, hasFill,
                             alpha)
            self._circlePair(-y + x0, -x + y0, y + x0, -x + y0, color, hasFill,
                             alpha)
            self._circlePair(-x + x0, -y + y0, x + x0, -y + y0, color, hasFill,
                             alpha)

            y += 1
            if radiusError < 0:
                radiusError += 2 * y + 1
            else:
                x -= 1
                radiusError += 2 * (y - x + 1)

    @timefunc
    def drawCircle(self, x, y, radius, color, alpha=None):
        self._circleHelper(x, y, radius, color, False, alpha)

    @timefunc
    def fillCircle(self, x, y, radius, color):
        self._circleHelper(x, y, radius, color, True)

    @timefunc
    def terminate(self):
        self.client.terminate()

    def _fillPolyRow(self, y, xs, color):
        # XXX: assume that the polygon is always convex or flat, never
        # concave. In this case, we always assume that the entire area
        # between min and max x gets filled with color. Except for the
        # case where there is just one pixel...
        if len(xs) == 1:
            self.buf.buf[self._clipx(xs[0]), y] = color
        else:
            begin = min(xs)
            end = max(xs)
            self.buf.buf[self._clipx(begin):self._clipx(end), y] = color

    @timefunc
    def fillPoly(self, points, color):
        """
        fill a flat or convex polygon.

        Specify all points in the path, and the closing edge will be automatically
        added for you.

        This function will not work for concave polygons. To achieve that, you
        should consider stacking several convex polygons next to one another.
        """
        # preserve the original
        points = list(points)
        # get a list of all of the points that bound the polygon
        edges = []
        prev = origin = points.pop(0)

        for x, y in points:
            edges.append(self._line(prev[0], prev[1], x, y))
            prev = (x, y)

        edges.append(self._line(prev[0], prev[1], origin[0], origin[1]))

        # we're going to process row by row, so first group the points by
        # row
        rows = {}
        xys = reduce(operator.add, edges)
        for xy in xys:
            rows.setdefault(xy[1], []).append(xy[0])

        # the xs in each row should have dups removed
        for y in list(map(int, rows.keys())):
            if y >= 0 and y < self.height:
                self._fillPolyRow(y, sorted(set(rows[y])), color)

    @timefunc
    def copyBuffer(self, buf):
        self.buf.copyImage(buf)
