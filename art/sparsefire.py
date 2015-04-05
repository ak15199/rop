from utils.fire import Gun

class Art(object):

    description = "Sparse Balistics"

    def __init__(self, matrix):
        self.gun = Gun(matrix)

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)

    def refresh(self, matrix):
        matrix.clear()
        self.gun.fire(matrix)

    def interval(self):
        return 100
