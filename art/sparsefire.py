from _baseclass import ArtBaseClass

from utils.fire import Gun


class Art(ArtBaseClass):

    description = "Sparse Balistics"

    def __init__(self, matrix, config):
        self.gun = Gun(matrix)

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)

    def refresh(self, matrix):
        matrix.clear()
        self.gun.fire(matrix)

    def interval(self):
        return 100
