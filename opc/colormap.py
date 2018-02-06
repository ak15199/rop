from utils import idw

from exceptions import AttributeError
import numpy as np


class Colormap(object):

    """
    Colormap management class
    """

    def __init__(self, size=None, palette=None):
        if size is not None:
            self.size = size
            self.cmap = np.empty((self.size, 3), dtype=np.uint8)
        elif palette is not None:
            self._buildPalette(palette)
        else:
            raise AttributeError("Invalid Colormap Initializer")

    def __len__(self):
        return self.size

    def flat(self, index0, index1, color):
        """
        initialize a block of colormap entries with a particular color
        """
        self.cmap[index0:index1] = color

    def _buildPalette(self, palette):
        index = 0
        oldcolor = None
        self.size = sum(palette.values())
        self.cmap = np.empty((self.size, 3), dtype=np.uint8)

        for color, count in palette.items():
            if oldcolor is None:
                oldcolor = color

            self.gradient(index, index+count, oldcolor, color)
            oldcolor = color
            index += count

    def gradient(self, index0, index1, color0, color1):
        """
        apply a linear gradient from color0 to color1 across a range of
        colormap cells
        """
        steps = float(index1) - index0
        delta = [(color1[gun] - color0[gun]) / steps for gun in range(3)]

        for index in range(index0, index1):
            c = [color0[gun] + delta[gun] * (index-index0) for gun in range(3)]
            self.cmap[index] = c

    def convert(self, point, scale=None):
        """
        Get the color associated with the given index. This method allows for
        scaling up or down, in the case where the desired range is either
        bigger or smaller than the colormap
        """
        if scale:
            point = point * self.size/scale

        index = int(min(self.size-1, max(0, point)))
        return self.cmap[index]

    def apply(self, data, scale=None):
        scale = self.size-1 if scale is None else scale
        return self.cmap[(data*scale).astype(np.int)]

    def soften(self, neighbors=1):
        """
        Use inverse distance weighting to soften the transitions between colors
        in the map, looking out by NEIGHBORS entries left and right.
        """
        self.cmap = idw.soften_2d(self.cmap, neighbors)

    def rotate(self, stepsize=1):
        """
        Rotate the colormap up or down by STEPSIZE places
        """

        # x3 since we have three colors to work with
        self.cmap = np.roll(self.cmap, stepsize*3)
