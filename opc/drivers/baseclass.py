class RopDriver(object):

    def __init__(self, width, height, address):
        raise NotImplementedError

    def send(self, packet):
        raise NotImplementedError

    def putPixels(self, channel, *sources):
        raise NotImplementedError

    def setFirmwareConfig(self, nodither=False, nointerp=False,
                          manualled=False, ledonoff=True):
        raise NotImplementedError

    def setGlobalColorCorrection(self, gamma, r, g, b):
        raise NotImplementedError

    def terminate(self):
        raise NotImplementedError
