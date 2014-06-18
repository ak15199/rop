from hue import rgbToHsv, hsvToRgb
import opc
from colors import BLACK

"""
This is loosely based on the Adafruit GFX library, although there
are a ton of differences. Some of the differences are where features
have not yet been implemented through necessity, but will be one day.

Others are additional effects that are here because they seemed
pretty cool. Like setting firmware configs on a connection, or
performing a HSV shift on the array.

check out text.py for text drawing.
"""

class OPCBuffer:
    """
    OPCBuffer can often be considered an internal class. But it
    comes in handy if you want to draw on a larger "virtual"
    array, and scale down for rendering on a physical array.
    """
    def __init__(self, numpix, color=BLACK):
        self.buffer = [color]*numpix

    def __getitem__(self, index):
        return self.buffer[index]

    def __setitem__(self, index, color):
        self.buffer[index] = color

    def __len__(self):
        return len(self.buffer)

    def __add___(self, other):
        pass

    def __or___(self, other):
        pass

    def __xor___(self, other):
        pass

    def __and___(self, other):
        pass

    def getPixels(self):
        return self.buffer

class OPCMatrix:
    def __init__(self, width, height, address, zigzag=False, pixelDebug=False):
        if address == None:
            self.client = None
        else:
            self.client = opc.Client(address)
            if not self.client.can_connect():
                print "can't conect to %s" % address
                exit(1)

        self.pixelDebug = pixelDebug
        self.width = width
        self.height = height
        self.buffer = OPCBuffer(self.numpix())
        self.zigzag = zigzag
        self.setCursor()

    def setFirmwareConfig(self, nodither=False, nointerp=False, manualled=False, ledonoff=True):
        self.client.setFirmwareConfig(nodither, nointerp, manualled, ledonoff)

    def numpix(self):
        return self.width * self.height

    def copy(self, source, x=None, y=None):
        if x == None and y == None:
            self._scaledCopy(source)
        else:
            self._panCopy(source, x, y)

    def _panCopy(self, source, ox, oy):
        for x in range(self.width):
            for y in range(self.height):
                src = source.getPixel(x + ox, y + oy)
                if src is not None:
                    self.drawPixel(x, y, src)

    def _scaledCopy(self, source):
        ratio = source.width / self.width
        if ratio < 1:
            return

        for x in range(self.width):
            for y in range(self.height):
                condensed = [0, 0, 0]
                for x0 in range(ratio):
                    for y0 in range(ratio):
                        src = source.getPixel(y0+x*ratio, y0+y*ratio)
                        for gun in range(3):
                            condensed[gun] = condensed[gun] + src[gun]

                for gun in range(3):
                    condensed[gun] = condensed[gun]/(ratio*ratio)

                self.drawPixel(x, y, condensed)

    def setCursor(self, pos=(0,0)):
        x, y = pos
        self.cursor = (x, y)

    def getCursor(self):
        return self.cursor

    def setStripPixel(self, z, color):
        self.buffer[z] = color

    def _getAddress(self, x, y):
        x, y = int(x), int(y)
        
        if x<0 or y<0 or x>=self.width or y>=self.height:
            if self.pixelDebug:
                raise Exception("Invaid Index (%d, %d)" % (x, y))
            else:
                return None

        if self.zigzag and y%2 == 1:
            x = (self.width-x)-1

        return x+y*self.width

    def getPixel(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            addr = self._getAddress(x, y)
            return self.buffer[addr]

        return None
        
    def drawPixel(self, x, y, color):
        addr = self._getAddress(x, y)
        if addr is not None:
            self.buffer[addr] = color

    def _clip(self, x, y):
        return (
                max(min(x, self.width), 0),
                max(min(y, self.height), 0),
            )

    def shift(self, dh=1.0, ds=1.0, dv=1.0):
        for i in range(self.numpix()):
            r = self.buffer[i][0]
            g = self.buffer[i][1]
            b = self.buffer[i][2]
            h, s, v = rgbToHsv(r, g, b)
            self.buffer[i] = hsvToRgb(h*dh, s*ds, v*dv)
                
    def fade(self, divisor):
        for i in range(self.numpix()):
            r = self.buffer[i][0] * divisor
            g = self.buffer[i][1] * divisor
            b = self.buffer[i][2] * divisor
            self.buffer[i] = (r, g, b)

    def clear(self, color=BLACK):
        self.buffer = OPCBuffer(self.numpix(), color)

    def show(self, channel=0):
        pixels = self.buffer.getPixels()
        self.client.put_pixels(pixels, channel=channel)

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
            ystep = 1;
        else:
            ystep = -1;

        points = []
        while x0 <= x1:
            if steep:
                points.append((y0, x0))
            else:
                points.append((x0, y0))
            x0 += 1

            err -= dy;
            if err < 0:
              y0 += ystep;
              err += dx;

        return points

    def drawLineRelative(self, x1, y1, color):
        path = self._line(x1, y1)
        for x, y in path:
            self.drawPixel(x, y, color)

    def drawLine(self, x1, y1, x2, y2, color):
        for x, y in self._line(x1, y1, x2, y2):
            self.drawPixel(x, y, color)

    def drawPoly(self, points, color):
        origin = points.pop(0)

        self.setCursor(origin)
        for point in points:
            x, y = point
            self.drawLineRelative(x, y, color)
        
        x, y = origin
        self.drawLineRelative(x, y, color)

    def fillRect(self, x1, y1, w, h, color):
        x1, y1 = int(x1), int(y1)
        w, h = int(w), int(h)
        x2, y2 = (x1+w-1, y1+h-1)
        x1, y1 = self._clip(x1, y1)
        x2, y2 = self._clip(x2, y2)

        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                self.drawPixel(x, y, color)

    def drawRect(self, x1, y1, w, h, color):
        self.drawPoly( [
                (x1, y1), (x1+w, y1), (x1+w, y1+h), (x1, y1+h)
            ], color)

