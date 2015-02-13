from __future__ import division

from utils.prof import timefunc


class RawClient(object):
    """
    Just pass back the raw data to the caller for rendering by the app
    """

    def __init__(self, server=None):
        pass

    def setGeometry(self, width, height):
        self.width = width
        self.height = height

    def putPixels(self, channel, pixels):
        return pixels

    def sysEx(self, systemId, commandId, msg):
        pass

    def setGlobalColorCorrection(self, gamma, r, g, b):
        pass

    def terminate(self):
        pass
