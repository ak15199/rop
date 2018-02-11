import colorsys
from math import fmod, sin, pi
from mwt import mwt
from .utils.prof import timefunc


@mwt(timeout=20)
@timefunc
def hsvToRgb(h, s=1.0, v=1.0, rainbow=True):
    """
    Convert a (h, s, v) value to the (r, g, b) color space. By default,
    we use a more cpu-intense method to curve the hue ramps above the
    typical linear, with a view to evening out the visible range of yellow,
    cyan, and purple.

    This method takes h, s, and v values in range 0..1 and returns r, g,
    and b values in range 0..255.
    """
    if rainbow:
        return [sin(c*pi/2)*255 for c in colorsys.hsv_to_rgb(h, s, v)]

    return [c*255 for c in colorsys.hsv_to_rgb(h, s, v)]


@mwt(timeout=20)
@timefunc
def rgbToHsv(r, g, b):
    """
    Convert a (r, g, b) value to the (h, s, v) color space. Note that
    presently, converting a rgb value to hsv and then back again will
    yield different results from the expected, because of the way in
    which color curves work in hsvToRgb

    This method takes r, g, and b values in range 0..255 and returns
    h, s, v values in range 0..1.
    """
    return colorsys.rgb_to_hsv(r/255, g/255, b/255)


@mwt(timeout=20)
def hue(shade):
    hue = shade * 255
    if hue < 85:
        return (hue * 3, 255 - hue * 3, 0)
    elif hue < 170:
        hue -= 85
        return (255 - hue * 3, 0, hue * 3)

    hue -= 170
    return (0, hue * 3, 255 - hue * 3)


def getColorGen(step=0.05, hue=0, sat=1, val=1):
    """
    Generator that returns a stream of shades as colors
    """
    hue = getHueGen(step, hue)
    while True:
        yield hsvToRgb(next(hue), sat, val)


def getHueGen(step=0.05, hue=0):
    """
    Generator that returns a stream of shades as hues
    """
    while True:
        hue = fmod(hue + step, 1)
        yield hue
