__author__ = 'rafe'

import logging
import itertools

try:
    import sdl2
except ImportError:
    raise ImportError('In order to use the SDL rop driver, must install PySDL2')
else:
    import sdl2.ext

from opc.drivers import baseclass

DISPLAY_WIDTH = 400

ASPECT_RATIO = 4, 6


class Driver(baseclass.RopDriver):

    def __init__(self, width, height, address):
        self.__width = width
        self.__height = height
        self.__address = address

        sdl2.ext.init()

        aw, ah = ASPECT_RATIO
        display_height = (DISPLAY_WIDTH * ah) / aw

        self.__window = sdl2.ext.Window('ROP', size=(DISPLAY_WIDTH, display_height))
        self.__window.show()

        self.__renderer = sdl2.ext.Renderer(self.__window)

        self.__space_width = DISPLAY_WIDTH / width
        self.__space_height = display_height / height

        self.__pixel_size = min(self.__space_width / 3, self.__space_height / 3)
        self.__inset_x = self.__space_width / 2 - self.__pixel_size / 2
        self.__inset_y = self.__space_height / 2 - self.__pixel_size / 2

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def address(self):
        return self.__address

    def putPixels(self, channel, *sources):
        renderer = self.__renderer
        renderer.clear()
        fill = renderer.fill
        pixel_size = self.__pixel_size
        space_height = self.__space_height
        space_width = self.__space_width
        inset_x = self.__inset_x
        inset_y = self.__inset_y
        for source in sources:
            for x, line in enumerate(source):
                for y, pixel in enumerate(line):
                    xx = x * space_width
                    yy = y * space_height
                    start_x = xx + inset_x
                    start_y = yy + inset_y
                    fill([start_x,
                          start_y,
                          pixel_size,
                          pixel_size],
                          pixel)
        renderer.present()

        # Need to drain the event loop.
        sdl2.ext.get_events()

    def sysEx(self, systemId, commandId, msg):
        logging.info('Received and ignoring sysex: id=%s commandId=%s\n%s',
                     systemId, commandId, msg)

    def setGlobalColorCorrection(self, gamma, r, g, b):
        logging.info(
            'Received and ignoring global color correction: (g, r, g, b) = (%s, %s, %s, %s)',
            gamma, r, g, b)

    def terminate(self):
        sdl2.ext.quit()
