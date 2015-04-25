from .. _baseclass import ArtBaseClass

from opc.text import OPCText, typeface_bbc


class ScrollText(ArtBaseClass):

    description = "Scroll text across the display"

    fg = None
    bg = None

    def __init__(self, matrix, config):
        self.config = config
        self._initText()
        self.thisMessage = self._getText()
        self.nextMessage = self._getText()

        self.typeface = OPCText(typeface_bbc)
        self.base = 0

    def _initText(self):
        raise NotImplementedError

    def _getText(self):
        raise NotImplementedError

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        matrix.clear()

        y = matrix.height/2 - 4

        end = self.typeface.drawText(matrix, 0-self.base, y,
                                     self.thisMessage, self.fg, self.bg)

        # drawText returns None if the image ran to the end of the page. If it
        # didn't, then it's time to bring in the new one.
        if end is not None:
            self.typeface.drawText(matrix, end, y,
                                     self.nextMessage, self.fg, self.bg)
            if end == 1:
                # this is the final pixel for the original text. So next time
                # through, next message is the active messge.
                self.thisMessage = self.nextMessage
                self.nextMessage = self._getText()
                self.base = -1

        self.base += 1

    def interval(self):
        return 50
