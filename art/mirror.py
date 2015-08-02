__author__ = 'rafe'

import colorsys

import PIL
from PIL import Image
from PIL import ImageChops
from PIL import ImageOps
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

    def __init__(self, matrix, config):
        self.brightness_threshold = config.get('BRIGHTNESS_THRESHOLD', 10)
        self.hue_rotation = config.get('COLOR_ROTATION', 0.02)

    def start(self, matrix):
        self.hue = 0.0

    def refresh(self, matrix):
        frame = get_frame()
        frame = frame.convert('L')
        frame = frame.rotate(90).resize((matrix.width, matrix.height), PIL.Image.BILINEAR)
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
        draw_pixel = matrix.drawPixel
        brightness_threshold = self.brightness_threshold
        for y in range(matrix.width):
            for x in range(matrix.height):
                r, g, b = image[x, y]
                if r > brightness_threshold or g > brightness_threshold or b > brightness_threshold:
                    draw_pixel(y, matrix.height - x, (r, g, b), 0.3)

    def interval(self):
        return 30

