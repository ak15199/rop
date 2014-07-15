class Colormap(object):

    """
    Colormap management class
    """

    def __init__(self, size):
        self.size = size
        self.cmap = [ (0, 0, 0) ] * size

    def gradient(self, index0, index1, color0, color1):
        steps = float(index1) - index0
        delta = [0] * 3
        for gun in range(3):
            delta[gun] = (color1[gun] - color0[gun]) / steps

        v = [0]*3
        for index in range(index0, index1):
            for gun in range(3):
                v[gun] = color0[gun] + delta[gun] * (index-index0)

            self.cmap[index] = v

    def convert(self, point, scale=None):
        if scale:
            point = point * self.size/scale

        index = int(min(self.size-1, max(0, point)))
        return self.cmap[index]
