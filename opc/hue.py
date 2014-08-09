import colorsys
from math import fmod
from utils.mwt import MWT
from utils.prof import timefunc

@MWT(timeout=20)
@timefunc
def hsvToRgb(h, s=1.0, v=1.0):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return r*255, g*255, b*255


@MWT(timeout=20)
@timefunc
def rgbToHsv(r, g, b):
    return colorsys.rgb_to_hsv(r/255, g/255, b/255)


def getHueGen(step=0.05, sat=1, val=1):
    hue = 0

    while True:
        hue = fmod(hue + step, 1)
        yield hsvToRgb(hue, sat, val)


@MWT(timeout=20)
def hue(shade):
    hue = shade * 255
    if hue < 85:
        return (hue * 3, 255 - hue * 3, 0)
    elif hue < 170:
        hue -= 85
        return (255 - hue * 3, 0, hue * 3)

    hue -= 170
    return (0, hue * 3, 255 - hue * 3)
