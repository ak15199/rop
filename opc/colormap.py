from utils import idw

from exceptions import AttributeError

def _newcolor():
    return [0]*3

class Colormap(object):

    """
    Colormap management class
    """

    def __init__(self, size=None, palette=None):
        if size is not None:
            self.size = size
            self.cmap = [_newcolor()] * self.size
        elif palette is not None:
            self._buildPalette(palette)
        else:
            raise AttributeError("Invalid Colormap Initializer")

    def flat(self, index0, index1, color):
        for index in range(index0, index1):
            self.cmap[index] = color

    def _buildPalette(self, palette):
        index = 0
        oldcolor = None
        self.size = sum(palette.values())
        self.cmap = [_newcolor()] * self.size

        for color, count in palette.iteritems():
            if oldcolor is None:
                oldcolor = color

            self.gradient(index, index+count, oldcolor, color)
            oldcolor = color
            index += count

    def gradient(self, index0, index1, color0, color1):
        steps = float(index1) - index0
        delta = _newcolor()
        for gun in range(3):
            delta[gun] = (color1[gun] - color0[gun]) / steps

        for index in range(index0, index1):
            v = _newcolor()
            for gun in range(3):
                v[gun] = color0[gun] + delta[gun] * (index-index0)

            self.cmap[index] = v

    def convert(self, point, scale=None):
        if scale:
            point = point * self.size/scale

        index = int(min(self.size-1, max(0, point)))
        return self.cmap[index]

    def soften(self, neighbors=1):
        idw.soften()
        for index in range(self.size):
            value = self.cmap[index]
            for n in neighbors:
                value = value/2 + (self.cmap[index-n] + self.cmap[index+n])

    def rotate(self, stepsize=1):
        self.cmap[:] = self.cmap[stepsize % self.size:] + self.cmap[:stepsize % self.size]
