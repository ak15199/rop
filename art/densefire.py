from _baseclass import ArtBaseClass

from utils.fire import Gun

class Art(ArtBaseClass):

    description = "Dense Balistics"

    def __init__(self, matrix, config):
        self.gun = Gun(matrix)

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)
        matrix.clear()

    def refresh(self, matrix):
        self.gun.fire(matrix)

    def interval(self):
        return 100
