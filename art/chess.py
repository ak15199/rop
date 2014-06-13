from opc.matrix import OPCMatrix

from random import randrange

class Art:

    def __init__(self, matrix):
        pass

    def start(self, matrix):
        matrix.fillRect(0,0,16,16,(96,64,24));
        matrix.drawRect(2,2,11,11,(128,128,128));

        for x in range(0, 8):
            for y in range(0, 8):
                black = (x&1) ^ (y&1);
                if black:
                    matrix.drawPixel(4+x,4+y, (192,0,0))
                else:
                    matrix.drawPixel(4+x,4+y, (0,0,192))

        matrix.show();

    def refresh(self, matrix):
        pass
  
    def interval(self):
        return 400
