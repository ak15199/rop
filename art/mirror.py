__author__ = 'rafe'

import PIL
from PIL import ImageChops
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


class Art(object):

    description = "Video Mirror"
    last_orig_frame = None

    def __init__(self, matrix, config):
        self.brightness_threshold = config.get('BRIGHTNESS_THRESHOLD', 10)

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        frame = get_frame().rotate(90).resize((matrix.width, matrix.height), PIL.Image.BILINEAR)
        last_frame = self.last_orig_frame
        self.last_orig_frame = frame
        if last_frame:
            frame = ImageChops.subtract(last_frame, frame, 0.05)
        image = numpy.asarray(frame.convert("RGB"))
        draw_pixel = matrix.drawPixel
        brightness_threshold = self.brightness_threshold
        for y in range(matrix.width):
            for x in range(matrix.height):
                r, g, b = image[x, y]
                if r > brightness_threshold or g > brightness_threshold or b > brightness_threshold:
                    draw_pixel(y, matrix.height - x, (r, g, b), 0.3)

    def interval(self):
        return 30

