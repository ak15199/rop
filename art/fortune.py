from baseclasses.scrolltext import ScrollText

from opc.colors import BLUE, WHITE
from random import randint
import os

FILE = "assets/fortunes.txt"


class Art(ScrollText):

    description = "Scroll classic fortunes across the display"

    fg = WHITE
    bg = BLUE

    def _initText(self):
        # TODO:catch file exceptions
        stats = os.stat(FILE)
        self.length = stats.st_size
        self.file = open(FILE, "U")

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

    def _getText(self):
        self._seekFortune()
        return self._readFortune()
