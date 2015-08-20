__author__ = 'rafe'

import colorsys
import os
import signal
import time

import PIL
from PIL import Image
from PIL import ImageChops
from PIL import ImageOps
from PIL import ImageDraw
import numpy

from art import rotator
from opc import matrix as matrix_module
from opc import buffer

try:
    import cv2  # Not for use on pi
except ImportError:
    import io
    import picamera
    camera = picamera.PiCamera(resolution=(50, 32), framerate=45)
    camera.start_preview(hflip=True)

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
        self.hue_rotation_min, self.hue_rotation_max = config.get('COLOR_ROTATION', (0.005, 0.1))
        self.fade_min, self.fade_max = config.get('FADE', (0.90, 0.99))
        self.event_generator = config.get('EVENTS', None)
        self.movement_timeout = config.get('MOVEMENT_TIMEOUT', 5)
        self.control_timeout = config.get('CONTROL_TIMEOUT', 2)
        self.rotator = rotator.Art(matrix, config.get('ARTS', {}))
        self.width = matrix.height
        self.height = matrix.width
        self.term_handler = signal.signal(signal.SIGTERM, self.term_handler)

        self.control_steps = self.height

        self.fade_range = self.fade_max - self.fade_min
        self.fade_step = self.fade_range / self.control_steps
        self.fade_index = int(self.control_steps / 2)

        self.hue_rotation_range = self.hue_rotation_max - self.hue_rotation_min
        self.hue_rotation_step = self.hue_rotation_range / self.control_steps
        self.hue_rotation_index = int(self.control_steps / 2)

        self._create_background_image()

        print 'Starting mirror at pid', os.getpid()

    def _create_background_image(self):
        background_image = Image.new('RGB', (self.width, self.height), (0, 0, 0))

        renderer = ImageDraw.Draw(background_image)
        for y in range(self.height):
            shade = (64 / self.height) * y
            renderer.line((0, y, self.width - 1, y), (shade, shade, shade))

        self.background = numpy.asarray(background_image)

    @property
    def fade(self):
        return self.fade_min + self.fade_step * self.fade_index

    @property
    def hue_rotation(self):
        return self.hue_rotation_min + self.hue_rotation_step * self.hue_rotation_index

    def term_handler(self, signum, stack):
        print 'TERM signal received'
        os.kill(os.getpid(), signal.SIGINT)
        if self.term_handler:
            self.term_handler(signum, stack)

    def start(self, matrix):
        self.hue = 0.0
        # The numpy.asarray function rotates the image, must invert axis.
        self.last_final_array = numpy.zeros((self.height, self.width, 3), dtype=int)
        self.last_move = 0
        self.rotator.start(matrix)
        self.showing = True
        self.last_control_time = 0

    def _receive_events(self):
        if self.event_generator:
            event = self.event_generator.next()
            while event:
                self.last_control_time = time.time()
                if event['event'] == 'inc':
                    if event['id'] == 1:
                        self.hue_rotation_index = max(0, self.hue_rotation_index - 1)
                    else:
                        self.fade_index = max(0, self.fade_index - 1)
                elif event['event'] == 'dec':
                    if event['id'] == 1:
                        self.hue_rotation_index = min(self.control_steps - 1,
                                                      self.hue_rotation_index + 1)
                    else:
                        self.fade_index = min(self.control_steps - 1,
                                              self.fade_index + 1)
                event = self.event_generator.next()

    def _render_controls(self):
        now = time.time()
        show = (now - self.last_control_time) <= self.control_timeout
        control_image = Image.new('RGB', (self.width, self.height))
        if not show:
            return control_image
        draw = ImageDraw.Draw(control_image)

        draw.fill = 255, 255, 255
        draw.rectangle([0, self.height - 1, 3, self.height - self.fade_index])
        draw.rectangle([self.width - 1, self.height - 1,
                        self.width - 4, self.height - self.hue_rotation_index])
        return control_image

    def refresh(self, matrix):
        self._receive_events()

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
        movement = bool(numpy.count_nonzero(image_mask))
        now = time.time()
        if movement:
            self.last_move = now
        seconds_since_movement = now - self.last_move
        show_mirror =  seconds_since_movement < self.movement_timeout

        if show_mirror:
            self.last_final_array = numpy.where(image_mask, image, faded)

            matrix.buf.buf = self.background | self.last_final_array
        else:
            if self.showing:
                matrix.buf.buf = numpy.empty(shape=(self.height, self.width, 3), dtype=buffer.DTYPE)
            self.rotator.refresh(matrix)
        matrix.buf.buf |= numpy.asarray(self._render_controls())
        self.showing = show_mirror

    def interval(self):
        if self.showing:
            return 30
        else:
            return self.rotator.interval()

