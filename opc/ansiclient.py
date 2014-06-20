ANSI_HOME = "\033[1;1H"
ANSI_CLEAR = "\033[J"
ANSI_RESTORE = "\033[0m"
ANSI_BRIGHT = "\033[1m"
ANSI_NORMAL = "\033[22m"

class Ansi_1(object):

    """
    Basic ansi controls and ten step ascii gradients.
    """

    MAP10 = " .:-=+*#%@"

    def __init__(self, ratio=1.1):
        # we use ratio to add some differentation between the guns
        self.ratio = ratio

    def _shortAnsi(self, v):
        return self.MAP10[min(9,max(v,0))]

    def convert(self, x, color):
        total = 0
        for v in color:
            total = v + self.ratio*total

        total /= 100

        return self._shortAnsi(int(total))

    def reset(self):
        return ""

class Ansi_2(Ansi_1):

    """
    An ansi client that supports 16 colors. This extends the basic ansi
    client, adding a few colors to the ascii art.
    """
    ANSI16_BRIGHT = 16
    ANSI16_BLACK = 0
    ANSI16_RED = 1
    ANSI16_GREEN = 2
    ANSI16_YELLOW = 3
    ANSI16_BLUE = 4
    ANSI16_MAGENTA = 5
    ANSI16_CYAN = 6
    ANSI16_WHITE = 7

    CODES = {
            "000":    ANSI16_BLACK,
            "001":    ANSI16_BLUE,
            "002":    ANSI16_BLUE+ANSI16_BRIGHT,
            "010":    ANSI16_GREEN,
            "011":    ANSI16_CYAN,
            "012":    ANSI16_CYAN,                  # approx
            "020":    ANSI16_GREEN+ANSI16_BRIGHT,
            "021":    ANSI16_CYAN,                  # approx
            "022":    ANSI16_CYAN+ANSI16_BRIGHT,
            "100":    ANSI16_RED,
            "101":    ANSI16_MAGENTA,
            "102":    ANSI16_MAGENTA,               # approx
            "110":    ANSI16_YELLOW,
            "111":    ANSI16_WHITE,
            "112":    ANSI16_BLUE+ANSI16_BRIGHT,    # approx
            "120":    ANSI16_YELLOW,                # approx
            "121":    ANSI16_GREEN+ANSI16_BRIGHT,   # approx
            "122":    ANSI16_CYAN+ANSI16_BRIGHT,    # approx
            "200":    ANSI16_RED+ANSI16_BRIGHT,
            "201":    ANSI16_RED+ANSI16_BRIGHT,     # approx
            "202":    ANSI16_MAGENTA+ANSI16_BRIGHT,
            "210":    ANSI16_YELLOW,                # approx
            "211":    ANSI16_RED+ANSI16_BRIGHT,     # approx
            "212":    ANSI16_MAGENTA+ANSI16_BRIGHT, # approx
            "220":    ANSI16_YELLOW+ANSI16_BRIGHT,
            "221":    ANSI16_YELLOW+ANSI16_BRIGHT,  # approx
            "222":    ANSI16_WHITE+ANSI16_BRIGHT,
        }

    def __init__(self):
        super(Ansi_2, self).__init__(1)

    def _ansi16_color(self, value):
        return "\033[" + str(30+value) + "m"

    def _ansi16_bright(self, bright):
        if bright:
            return ANSI_BRIGHT

        return ANSI_NORMAL

    def convert(self, x, color):
        result = ""
        if x == 0:
            self.lastshade = None
            self.lastbright = None

        # build an array describing a down-sampled version of the
        # color as a three character string, with each gun being
        # described with a [012] value
        map = "".join([ str(int(round(v/128))) for v in color ])
        code = self.CODES[map]
        shade = code & 7
        bright = (code & 16) != 0

        if self.lastshade != shade:
            result += self._ansi16_color(shade)
        if self.lastbright != bright:
            result += self._ansi16_bright(bright)

        self.lastshade = shade
        self.lastbright = bright
        
        return result + super(Ansi_2, self).convert(x, color)

    def reset(self):
        return ANSI_RESTORE

class AnsiClient:
    """
    Simple text based client that displays a LED string as asciiart. There
    are several versions that can be specified, each requiring a varying
    degree of functionality from the terminal. See the specific
    implementations for details.

    TODO: Although not all terminal emulators support this more advanced
            version would use the xterm-256 color set, presumably as an
            Ansi-3 class.
    """

    clients = {
            "ansi": Ansi_1,
            "ansi-1": Ansi_1,
            "ansi-2": Ansi_2,
        }

    def __init__(self, width, height, address):
        self.width = width
        self.height = height

        self.converter = self.clients[address]()

    def show(self, pixels):
        print ANSI_HOME+ANSI_CLEAR
        print " + " + "-"*self.width + " +"

        for y in range(self.height):
            row = [ self.converter.convert(x, pixels[x+y*self.height]) for x in range(self.width) ]

            print ' | ' + ''.join(row) + self.converter.reset() + ' |'

        print " + " + "-"*self.width + " +"
        
