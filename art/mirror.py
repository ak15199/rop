__author__ = 'rafe'

import colorsys

import time

import PIL
from PIL import Image
from PIL import ImageChops
from PIL import ImageOps
import numpy

from opc import matrix as matrix_module

try:
    import cv2
except ImportError:
    import io
    import picamera
    camera = picamera.PiCamera(resolution=(50, 32), framerate=45)
#    camera.start_preview(hflip=True)

    def get_frame():
        stream = io.BytesIO()
        camera.capture(stream, format='png', use_video_port=True)
        stream.seek(0)
        return Image.open(stream)
else:
    capture = cv2.VideoCapture(0)
    def get_frame():
        _, bgr = capture.read()
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb)


class Art(object):

    description = "Video Mirror"
    last_orig_frame = None
    last_final_array = None

    def __init__(self, matrix, config):
        self.brightness_threshold = config.get('BRIGHTNESS_THRESHOLD', 10)
        self.hue_rotation = config.get('COLOR_ROTATION', 0.02)
        self.fade = config.get('FADE', 0.95)
        self.width = matrix.height
        self.height = matrix.width

    def start(self, matrix):
        self.hue = 0.0
        # The numpy.asarray function rotates the image, must invert axis.
        self.last_final_array = numpy.zeros((self.height, self.width, 3), dtype=int)

    def refresh(self, matrix):
        frame = get_frame()
        frame = frame.convert('L')
        frame = frame.resize((self.width, self.height), PIL.Image.BILINEAR)

        last_frame = self.last_orig_frame
        self.last_orig_frame = frame
        if last_frame:
            frame = ImageChops.subtract(last_frame, frame, 0.05)

        r, g, b = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
        self.hue += self.hue_rotation
        if self.hue > 1.0:
            self.hue -= 1.0
        if self.hue < 0.0:
            self.hue += 1.0
        r = int(r * 256)
        g = int(g * 256)
        b = int(b * 256)
        frame = ImageOps.colorize(frame, (0, 0, 0), (r, g, b)).convert('RGB')

        image = numpy.asarray(frame)
        faded = (self.last_final_array * self.fade).astype(matrix_module.DTYPE)
        image_mask = numpy.any(image > self.brightness_threshold, axis=2, keepdims=True)
        self.last_final_array = numpy.where(image_mask, image, faded)
        matrix.buf.buf = self.last_final_array

    def interval(self):
        return 30

