from _baseclass import ArtBaseClass

import requests

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

    def start(self, matrix):
        matrix.clear()

    def _load(self, matrix):
        try:
            r = requests.get(self.url)
            if r.status_code == 200:
                self.image = Image(bytestream=r.content)
            else:
                self.image = Image(filename="assets/images/lena.jpg")
        except Exception:
            self.image = Image(filename="assets/images/lena.jpg")

        self.position = position(matrix, self.image)

    def refresh(self, matrix):
        try:
            x, y = self.position.next()
        except:
            self._load(matrix)
            x, y = self.position.next()

        buf = self.image.translate(matrix, scale=1, x=x, y=y)
        matrix.copyBuffer(buf)

    def interval(self):
        return 40
