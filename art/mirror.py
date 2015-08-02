__author__ = 'rafe'

import PIL
from PIL import ImageChops
from PIL import ImageEnhance
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
    last_orig_frame = None
    last_xform_frame = None

    def __init__(self, matrix, config):
        pass

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        frame = get_frame().rotate(90).resize((matrix.width, matrix.height), PIL.Image.BILINEAR)
        last_frame = self.last_orig_frame
        self.last_orig_frame = frame
        if last_frame:
            frame = ImageChops.subtract(last_frame, frame, 0.1)
            xform_frame = self.last_xform_frame
            if xform_frame:
                enhancer = ImageEnhance.Brightness(xform_frame)
                xform_frame = enhancer.enhance(0.9)
                frame = ImageChops.add(frame, xform_frame)
            self.last_xform_frame = frame
        image = numpy.asarray(frame)
        draw_pixel = matrix.drawPixel
        for y in range(matrix.width):
            for x in range(matrix.height):
                rgb = image[x, y][:3]  # May need to strip alpha channel
                draw_pixel(y, matrix.height - x, rgb, 0.3)

    def interval(self):
        return 30

