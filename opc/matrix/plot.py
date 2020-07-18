from functools import reduce
import numpy as np
import operator

from ..utils.prof import timefunc


class Plot(object):

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
