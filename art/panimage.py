from ._baseclass import ArtBaseClass

import requests

try:
    from thread import start_new_thread, allocate_lock
except:
    from _thread import start_new_thread, allocate_lock

import logging

from opc.image import Image


def position(matrix, image):
    x = 0
    y = 0

    while y < (image.height-matrix.height):
        while x < image.width-matrix.width:
            yield x, y
            x += 1

        dy = 0
        while dy < matrix.height and y < (image.height-matrix.height):
            yield x, y
            y += 1
            dy += 1

        while x > 0 and y < (image.height-matrix.height):
            yield x, y
            x -= 1

        dy = 0
        while dy < matrix.height and y < (image.height-matrix.height):
            yield x, y
            y += 1
            dy += 1


class Art(ArtBaseClass):

    description = "Grab random images from the internet and pan over them"

    def __init__(self, matrix, config):
        w = matrix.width*16
        h = matrix.height*16
        self.url = "http://lorempixel.com/%s/%d/" % (w, h)

        self.image_active = None
        self._load()

    def start(self, matrix):
        matrix.clear()

    def _load(self):
        self.image_loaded = None
        start_new_thread(Art._loadthread, (self,))

    def _consume(self, matrix):
        if not self.image_loaded:
            return False

        self.image_active = self.image_loaded
        self._load()

        self.position = position(matrix, self.image_active)

        return True

    def _loadthread(self):
        logging.info("_loadthread begin")
        try:
            r = requests.get(self.url)
            if r.status_code == 200:
                self.image_loaded = Image(bytestream=r.content)
            else:
                logging.error("_loadthread   code %d, using fallback"%r.status_code)
                self.image_loaded = Image(filename="assets/images/lena.jpg")
        except Exception as e:
            logging.error("_loadthread   exception '%s', using fallback"%str(e))
            self.image_loaded = Image(filename="assets/images/lena.jpg")

    def refresh(self, matrix):
        if not self.image_active:  # no image is active
            if not self._consume(matrix):  # can we get a fresh image?
                return  # return and re-try next cycle if still pending

        try:
            x, y = next(self.position)
        except:
            self.image_active = False  # borked over image end
            return # try and load new image next cycle

        buf = self.image_active.translate(matrix, scale=1, x=x, y=y)
        matrix.copyBuffer(buf)

    def interval(self):
        return 40
