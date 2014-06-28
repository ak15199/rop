from frange import frange
from random import random
from copy import copy

class Region:

    def __init__(self, x0, y0, x1, y1):
        self.x0, self.y0 = x0, y0
        self.x1, self.y1 = x1, y1

    def __str__(self):
        return "(%f, %f, %f, %f)" % (self.x0, self.y0, self.x1, self.y1)

    def dxdy(self, dx, dy):
        return (self.x1-self.x0)/dx, (self.y1-self.y0)/dy

    def portion(self, x, y, d):
        d += 0.0
        dx, dy = self.dxdy(d, d)
        region = Region(
                self.x0+dx*x, self.y0+dy*y,
                self.x0+dx*(x+1), self.y0+dy*(y+1),
            )
        
        return region

    def delta(self, theirs, steps=1):
        steps += 0.0
        return Region(
                (theirs.x0-self.x0)/steps, 
                (theirs.y0-self.y0)/steps, 
                (theirs.x1-self.x1)/steps, 
                (theirs.y1-self.y1)/steps, 
            )
    
    def increment(self, delta):
        self.x0, self.y0 = self.x0+delta.x0, self.y0+delta.y0
        self.x1, self.y1 = self.x1+delta.x1, self.y1+delta.y1

    def _feq(self, a, b, epsilon=0.00000001):
        return abs(a - b) < epsilon

    def __eq__(self, theirs):
        return isinstance(theirs, Region)  and  \
             self._feq(theirs.x0, self.x0) and  \
             self._feq(theirs.y0, self.y0) and  \
             self._feq(theirs.x1, self.x1) and  \
             self._feq(theirs.y1, self.y1)      
    
class Mandelbrot:

    def __init__(self, width, height, maxsteps):
        self.width = width
        self.height = height
        self.maxsteps = maxsteps
        self.detail = [[0 for y in range(self.height)] for x in range(self.width)]

    def _point(self, x, y):
        n, u, v = 0, x, y
        
        while True:
            a, b = u*u, v*v
            if a+b >= 4:
                return n

            n += 1
            if n == self.maxsteps:
                return None

            v, u = 2*u*v+y, a-b+x

    def draw(self, region):
        dx, dy = region.dxdy(self.width, self.height)

        total = 0
        x_range = range(self.width)
        y_range = range(self.height)

        for x in x_range:
            for y in y_range:
                point = self._point(region.x0+dx*x, region.y0+dy*y)
                self.detail[x][y] = point
                if point is not None:
                    total += point

        return self.detail

    def _gradient(self, x, y, interval):
        """
        calculate the gradient for a given quadrant
        """
        imax = 0
        imin = self.maxsteps
        found = False
        hasnone = False

        dx = self.width / interval
        dy = self.height / interval

        x0, y0 = int(dx*x), int(dy*y)
        x1, y1 = int(dx*(x+1))-1, int(dy*(y+1))-1

        for x in range(x0, x1):
            for y in range(y0, y1):
                point = self.detail[x][y]
                if point is None:
                    hasnone = True
                else:
                    found = True
                    imax = max(point, imax)
                    imin = min(point, imin)

        # if the quadrant is all black then we didn't find jack. Also, if
        # it's all just one color, then that really isn't any better.
        if not found or imin == imax:
            return 0

        # quadrants with some black though, are definitely preferable
        if hasnone:
            imax += 3

        return (imax - imin) 
    
    def mostInteresting(self, area):
        """
        determine which quadrant has the steepest iteration count
        gradient. 
        """
        INTERVAL = 4
        grad_max = 0
        region = None

        quadrant = 0
        for tx in range(0, INTERVAL):
            for ty in range(0, INTERVAL):
                quadrant += 1
                grad = self._gradient(tx, ty, INTERVAL)
                # if it's close, then it's in with a chance
                lucky = grad_max and (grad/grad_max) > .9 and random()>0.6
                close = grad_max == grad and random()>0.6
                if grad > grad_max or lucky or close:
                    grad_max = grad
                    chosen = quadrant
                    region = area.portion(tx, ty, INTERVAL)

        if grad_max < 2:
            return None

        return region
