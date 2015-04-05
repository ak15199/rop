from utils.fire import Gun

class Art(object):

    description = "Dense Balistics"

    def __init__(self, matrix):
        self.gun = Gun(matrix)

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)
        matrix.clear()

    def refresh(self, matrix):
        self.gun.fire(matrix)

    def interval(self):
        return 100
