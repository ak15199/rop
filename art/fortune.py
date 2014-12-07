from opc.colors import BLUE
from opc.text import OPCText, typeface_bbc
from random import randint
import os

FILE = "assets/fortunes.txt"


class Art(object):

    description = "Scroll classic fortunes across the display"

    def _seekFortune(self):
        index = randint(0, self.length)
        self.file.seek(index)
        while self.file.readline()[0] != "%":
            pass

    def _readFortune(self):
        buffer = "+++ "
        while True:
            line = self.file.readline()
            if line == "":
                if buffer == "":
                    # we teleported to the end of the file. Try again.
                    return self._getFortune()
                else:
                    # we have a fortune, but reached EOF. We're good.
                    return buffer

            # Replace line termination with a space
            line = line[:-1]+" "

            if line == "% ":
                return buffer

            buffer += line.replace("\t", "  ")

    def _getFortune(self):
        self._seekFortune()
        return self._readFortune()

    def __init__(self, matrix):
        stats = os.stat(FILE)
        self.length = stats.st_size

        self.file = open(FILE, "U")
        self.thisMessage = self._getFortune()
        self.nextMessage = self._getFortune()

        self.typeface = OPCText(typeface_bbc)
        self.base = 0

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)

    def refresh(self, matrix):
        matrix.clear()

        y = matrix.height/2 - 4

        end = self.typeface.drawText(matrix, 0-self.base, y,
                                     self.thisMessage, (192, 192, 255), BLUE)

        # drawText returns None if the image ran to the end of the page. If it
        # didn't, then it's time to bring in the new one.
        if end is not None:
            self.typeface.drawText(matrix, end, y, self.nextMessage,
                                   (192, 192, 255), BLUE)
            if end == 1:
                # this is the final pixel for the original text. So next time
                # through, next message is the active messge.
                self.thisMessage = self.nextMessage
                self.nextMessage = self._getFortune()
                self.base = -1

        self.base += 1

    def interval(self):
        return 80
