import numpy as np
from PIL import Image as PI
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from .utils.prof import timefunc


class Image(object):

    def __init__(self, filename=None, bytestream=None):
        if filename is not None:
            image = PI.open(filename).rotate(-90, PI.BICUBIC).convert('RGB')
            self.image = image

        if bytestream is not None:
            self.image = PI.open(StringIO.StringIO(bytestream))

        self.width, self.height = self.image.size

    @timefunc
    def translate(self, matrix, scale=0, x=0, y=0):
        i = self.image.copy()
        if scale == 0:
            i = self.image.resize((matrix.height, matrix.width), PI.ANTIALIAS)
        else:
            i = self.image.resize((int(self.height/scale),
                                   int(self.width/scale)), PI.ANTIALIAS)

        return np.asarray(i.crop((y, x, y+matrix.height, x+matrix.width)))
