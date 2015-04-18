from copy import deepcopy
import colorsys
import operator
import Image
import numpy as np

from colors import BLACK
from hue import rgbToHsv, hsvToRgb
import nphue

from buffer import OPCBuffer
from ansiclient import AnsiClient
from rawclient import RawClient
from fastopc import FastOPC as OpcClient

from utils.prof import timefunc


DTYPE = np.uint8

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
    This is loosely based on the Adafruit GFX library, although there
    are a ton of differences. Some of the differences are where features
    have not yet been implemented through necessity, but will be one day.

    Others are additional effects that are here because they seemed
    pretty cool. Like setting firmware configs on a connection, or
    performing a HSV shift on the array.

    check out the additional classes in this module for more code, and
    see the examples provided for usage.
    """

    HQMULT = 4

    @timefunc
    def __init__(self, width, height, address,
            zigzag=False, flipud=False, fliplr=False):
        """
        width -- renderable width
        height -- renderable height
        address -- display type, or OPC address. Type is ansi, raw, or None
        zigzag -- set to true if alternate rows travel opposite directions
        flipud -- top is bottom
        fliplr -- left is right
        """

        self.internal = address is None

        self.buf_std = OPCBuffer(width, height)
        # only "real" displays get a high quality option
        if self.internal:
            self.buf_hq = self.buf_std
        else:
            self.buf_hq = OPCBuffer(width*self.HQMULT, height*self.HQMULT)

        self.hq(False)

        if self.internal:
            self.client = None
        elif address[0:4] == 'ansi':
            self.client = AnsiClient(address)
            self.client.setGeometry(width, height)
            self.zigzag = False
            self.flipud = False
            self.fliplr = False
        elif address[0:3] == 'raw':
            self.client = RawClient()
            self.client.setGeometry(width, height)
            self.zigzag = False
            self.flipud = False
            self.fliplr = True
        else:
            self.client = OpcClient(address)
            self.zigzag = zigzag
            self.flipud = flipud
            self.fliplr = fliplr

        self.setCursor()

    @timefunc
    def hq(self, ishq=True):
        if ishq and not self.internal:
            self.ishq = ishq
            self.buf = self.buf_hq
        else:
            self.ishq = False
            self.buf = self.buf_std

        self.width = self.buf.width
        self.height = self.buf.height
        self.numpix = self.width * self.height
        self.midWidth = self.width / 2.0
        self.midHeight = self.height / 2.0

    @timefunc
    def setFirmwareConfig(self, nodither=False, nointerp=False,
                          manualled=False, ledonoff=True):

        if self.client is not None:
            data = chr(nodither | (nointerp << 1) | (manualled << 2) |
                       (ledonoff << 3))
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
            self.buf.scaledCopy(source.buf)
        else:
            self.buf.panCopy(source.buf, x, y)

    def _clipx(self, x):
        return max(min(x, self.width-1), 0)

    def _clipy(self, y):
        return max(min(y, self.height-1), 0)

    @timefunc
    def _clip(self, x, y):
        return (self._clipx(x), self._clipy(y))

    @timefunc
    def shift(self, dh=1.0, ds=1.0, dv=1.0):
        """
        Shift any of hue, saturation, and value on the matrix, specifying
        the attributes that you'd like to adjust
        """
        hsv = nphue.rgb_to_hsv(self.buf.buf)
        mod = hsv * np.array([dh, ds, dv])
        rgb = nphue.hsv_to_rgb(mod)

        self.buf.buf = rgb

    @timefunc
    def fade(self, divisor):
        """
        Special case of shift for just value that'll be faster than doing it
        the long way.
        """
        buf = self.buf.buf * divisor
        self.buf.buf = buf.astype(dtype=DTYPE)

    def soften(self):
        """Soften influence pixel color from our neighbors"""
        self.buf.blur()

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
    def drawPixel(self, x, y, color, alpha=None):
        """
        Set the pixel tuple at the specified location.  Perform no operation
        if the color value is None, or the address out of bounds
        """
        if x >= self.width or y >= self.height or \
                x < 0 or y < 0 or color is None:
            return

        if alpha is None:
            self.buf.buf[x, y] = color
        else:
            a0 = alpha
            a1 = 1-alpha
            self.buf.buf[x, y] = np.asarray(color)*a0 + self.buf.buf[x, y]*a1

    @timefunc
    def drawPixels(self, coords, color, alpha=None):
        """
        Set the pixel tuple at the set of specified locations.  Like drawPixel,
        but operates over a list of (x, y) coordinates.
        """
        coords = [(coord[0], coord[1]) for coord in coords if
                  coord[0] >= 0 and coord[0] < self.width and
                  coord[1] >= 0 and coord[1] < self.height]

        if not coords: # when everything is off screen
            return

        xs, ys = zip(*coords)

        if alpha is None:
            self.buf.buf[xs, ys] = color
        else:
            a0 = alpha
            a1 = 1-alpha
            self.buf.buf[xs, ys] = np.asarray(color)*a0 + self.buf.buf[xs, ys]*a1

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
                points.append((y1, x1))
            else:
                points.append((x1, y1))

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
        return self.cursor[0]!=x or self.cursor[1]!=y

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
        if int(x1) == int(x2) or int(y1) == int(y2):
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
        Draw a filled rectangle
        """
        x1, y1 = int(x1), int(y1)
        w, h = int(w), int(h)
        x2, y2 = (x1+w-1, y1+h-1)

        self.fillRectAbsolute(x1, y1, x2, y2, color)

    @timefunc
    def drawRect(self, x1, y1, w, h, color):
        """
        Draw a rectangle
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
        try:
            self.client.terminate()
        except AttributeError:
            pass  # pass if it's a non-ansi client

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
        fill a flat or convex polygon. This will not work for concave
        polygons. In order to achieve that goal, you should consider
        stacking several polygons next to one another
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
        for y in rows.keys():
            if y >= 0 and y < self.height:
                self._fillPolyRow(y, sorted(set(rows[y])), color)

    @timefunc
    def drawImage(self, filename, scale=1, x=0, y=0):
        i = Image.open(filename).rotate(-90, Image.BICUBIC)
        i = i.resize((self.width, self.height), Image.ANTIALIAS)

        self.buf.copyImage(i)
