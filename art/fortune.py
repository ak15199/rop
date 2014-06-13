from opc.colors import *
from opc.hue import hsvToRgb
from opc.matrix import OPCMatrix
from opc.text import OPCText, typeface_bbc
from random import randint, seed
import os
from time import time

FILE = "assets/fortunes.txt"

class Art:

    def _seekFortune(self):
        index = randint(0, self.length)
        print "seek fortune", index
        self.file.seek(index)
        while self.file.readline()[0] != "%":
            pass

    def _readFortune(self):
        print "read fortune"
        buffer = ""
        while True:
            line = self.file.readline()
            if line == "":
                if buffer == "":
                    # we teleported to the end of the file. Try again.
                    return _self.getFortune()
                else:
                    # we have a fortune, but reached EOF. We're good.
                    return buffer 

            # Replace last character ('\n') with a space
            line = line[:-1] + " "
            
            if line == "%":
                return buffer 

            buffer += line

    def _getFortune(self):
        self._seekFortune()
        return self._readFortune()
        
    def __init__(self, matrix):
        seed(time)
        stats = os.stat(FILE);
        self.length = stats.st_size

        self.file = open(FILE, "r")
        self.message = self._getFortune()
        self.typeface = OPCText(typeface_bbc)
        self.base = 0

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)
    
    def refresh(self, matrix):
        matrix.clear()

        end = self.typeface.drawText(matrix, 0-self.base, 5, self.message, (192, 192,255), BLUE)
        if end is not None:
            # if the text finishes part way across the display, then do it again!
            self.typeface.drawText(matrix, end, 5, self.message, (192, 192, 255), BLUE)
            if end == 1:
                self.base = -1

        self.base += 1

    def interval(self):
        return 80

