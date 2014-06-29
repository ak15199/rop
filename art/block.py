from opc.matrix import OPCMatrix

from random import randrange

class Art:

    def __init__(self, matrix):
        pass

    def start(self, matrix):
        matrix.clear()

    def refresh(self, matrix):

        matrix.fade(0.95)

        color = (randrange(0, 256), randrange(0, 256), randrange(0, 256))
        min = 2
        max = 7

        matrix.fillRect(
            randrange(0, matrix.width),
            randrange(0, matrix.height),
            randrange(min, max),
            randrange(min, max),
            color,
            )
  
    def interval(self):
        return 400

