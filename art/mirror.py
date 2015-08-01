__author__ = 'rafe'

import PIL
import numpy

try:
    import cv2
except ImportError:
    import io
    import picamera
    camera = picamera.PiCamera()
    camera.resolution = 50, 32
    def get_frame():
        stream = io.BytesIO()
        camera.capture(stream, format='png', use_video_port=True)
        stream.seek(0)
        return PIL.Image.open(stream)
else:
    capture = cv2.VideoCapture(0)
    def get_frame():
        _, bgr = capture.read()
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        return PIL.Image.fromarray(rgb)


import contextlib
import time
@contextlib.contextmanager
def timeit():
    start = time.time()
    try:
        yield start
    finally:
        print '%03f' % (time.time() - start)


class Art(object):

    description = "Video Mirror"

    def __init__(self, matrix, config):
        pass

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        frame = get_frame().rotate(90).resize((matrix.width, matrix.height), PIL.Image.BILINEAR)
        image = numpy.asarray(frame)
        draw_pixel = matrix.drawPixel
        for y in range(matrix.width):
            for x in range(matrix.height):
                rgb = image[x, y][:3]  # May need to strip alpha channel
                draw_pixel(x, y, rgb, 0.3)

    def interval(self):
        return 30

