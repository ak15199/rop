from opc.drivers.baseclass import RopDriver


class Driver(RopDriver):
    """
    Just pass back the raw data to the caller for rendering by the app
    """

    def __init__(self, width, height, address):
        pass

    def putPixels(self, channel, pixels):
        return pixels

    def sysEx(self, systemId, commandId, msg):
        pass

    def setGlobalColorCorrection(self, gamma, r, g, b):
        pass

    def terminate(self):
        pass
