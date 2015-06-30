__author__ = 'rafe'

import PIL
import numpy

try:
    import cv2
except ImportError:
    raise ImportError('Must install cv2 for video to work.  PiCamera coming soon.')

capture = cv2.VideoCapture(0)

def get_frame():
    _, bgr = capture.read()
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return PIL.Image.fromarray(rgb)


class Art(object):

    description = "Video Mirror"

    def __init__(self, matrix, config):
        pass

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        frame = get_frame().rotate(90).resize((matrix.width, matrix.height), PIL.Image.BILINEAR)
        image = numpy.asarray(frame)
        for y in range(matrix.width):
            for x in range(matrix.height):
                matrix.drawPixel(x, y, image[x, y], 0.3)

    def interval(self):
        return 30

