#encoding: utf-8

import curses

from error import TtyTooSmall


def initCurses():
    global stdscr

    stdscr = curses.initscr()
    curses.start_color()


def exitCurses():
    curses.endwin()


class Ansi_0(object):

    def __init__(self):
        pass

    def convert(self, x, color):
        pass


class Ansi_1(Ansi_0):

    MAP10 = " .:-=+*#%@"    # ten step asciiart gradient
    MAP8 = u" ⡀⢂⢌⢕⡫⢷⣽⣿"     # nine step braille gradient, but
                            # don't even bother before python 3.3
                            # and libncursesw.so.5

    def __init__(self, ratio=1.1):
        # we use ratio to add some differentation between guns
        self.ratio = ratio

    def _shortAnsi(self, v, chars):
        return chars[min(len(chars)-1, max(v, 0))]

    def _convert(self, x, color, chars):
        if chars is None:
            chars = self.MAP10

        total = 0
        for v in color:
            total = v + self.ratio*total

        total /= 100

        return self._shortAnsi(int(total), chars)

    def convert(self, x, color, chars=None):
        stdscr.addstr(self._convert(x, color, chars))


class Ansi_2(Ansi_1):

    """
    An ansi client that supports 16 colors. This extends the basic implementation,
    adding some color to the ascii art.
    """
    def __init__(self):
        super(Ansi_2, self).__init__(1)

        COLOR_WHITE = 0  # curses has white locked in postition 0
        COLOR_BLACK = 1
        COLOR_RED = 2
        COLOR_GREEN = 3
        COLOR_YELLOW = 4
        COLOR_BLUE = 5
        COLOR_MAGENTA = 6
        COLOR_CYAN = 7

        self.CODES = {
                "000":    curses.color_pair(COLOR_BLACK),
                "001":    curses.color_pair(COLOR_BLUE),
                "002":    curses.color_pair(COLOR_BLUE)+curses.A_BOLD,
                "010":    curses.color_pair(COLOR_GREEN),
                "011":    curses.color_pair(COLOR_CYAN),
                "012":    curses.color_pair(COLOR_CYAN),                   # approx
                "020":    curses.color_pair(COLOR_GREEN)+curses.A_BOLD,
                "021":    curses.color_pair(COLOR_CYAN),                   # approx
                "022":    curses.color_pair(COLOR_CYAN)+curses.A_BOLD,
                "100":    curses.color_pair(COLOR_RED),
                "101":    curses.color_pair(COLOR_MAGENTA),
                "102":    curses.color_pair(COLOR_MAGENTA),                # approx
                "110":    curses.color_pair(COLOR_YELLOW),
                "111":    curses.color_pair(COLOR_WHITE),
                "112":    curses.color_pair(COLOR_BLUE)+curses.A_BOLD,     # approx
                "120":    curses.color_pair(COLOR_YELLOW),                 # approx
                "121":    curses.color_pair(COLOR_GREEN)+curses.A_BOLD,    # approx
                "122":    curses.color_pair(COLOR_CYAN)+curses.A_BOLD,     # approx
                "200":    curses.color_pair(COLOR_RED)+curses.A_BOLD,
                "201":    curses.color_pair(COLOR_RED)+curses.A_BOLD,      # approx
                "202":    curses.color_pair(COLOR_MAGENTA)+curses.A_BOLD,
                "210":    curses.color_pair(COLOR_YELLOW),                 # approx
                "211":    curses.color_pair(COLOR_RED)+curses.A_BOLD,      # approx
                "212":    curses.color_pair(COLOR_MAGENTA)+curses.A_BOLD,  # approx
                "220":    curses.color_pair(COLOR_YELLOW)+curses.A_BOLD,
                "221":    curses.color_pair(COLOR_YELLOW)+curses.A_BOLD,   # approx
                "222":    curses.color_pair(COLOR_WHITE)+curses.A_BOLD,
            }

        color = [
                curses.COLOR_WHITE,
                curses.COLOR_BLACK,
                curses.COLOR_RED,
                curses.COLOR_GREEN,
                curses.COLOR_YELLOW,
                curses.COLOR_BLUE,
                curses.COLOR_MAGENTA,
                curses.COLOR_CYAN,
            ]

        for index in range(1, 8):
            curses.init_pair(index, color[index], curses.COLOR_BLACK)

    def _cursesAttr(self, color):
        """
        build an array describing a down-sampled version of the
        color as a three character string, with each gun being
        described with a value in the range 0..2, then map this to attrs
        """
        map = "".join([str(int(round(v/128))) for v in color])
        return self.CODES[map]

    def convert(self, x, color, chars=None):
        stdscr.addstr(super(Ansi_2, self)._convert(x, color, chars), self._cursesAttr(color))


class AnsiClient:
    """
    Simple text based client that displays a LED string as asciiart. There
    are several ways to do this, depending on the capability level of the
    terminal. See the specific implementations for details.

    TODO: add support for xterm-256
    """

    def __init__(self, width, height, address):
        self.width = width
        self.height = height

        initCurses()
        stdscr.clear()
        if curses.has_colors():
            self.converter = Ansi_2()
        else:
            self.converter = Ansi_1()

    def _show(self, pixels):
        stdscr.addstr(0, 0, " + " + "-"*self.width + " +\n")

        for y in reversed(range(self.height)):
            stdscr.addstr(" | ")
            for x in range(self.width):
                self.converter.convert(x, pixels[x+y*self.width])

            stdscr.addstr(" | \n")

        stdscr.addstr(" + " + "-"*self.width + " +\n")

        stdscr.refresh()

    def show(self, pixels):
        try:
            self._show(pixels)
        except curses.error as e:
            ttyheight, ttywidth = stdscr.getmaxyx()
            message = \
                "Your screen (%d, %d) is too small to support this size matrix (%d, %d)" % (ttywidth, ttyheight, self.width, self.height)

            raise TtyTooSmall(message)

    def terminate(self):
        exitCurses()
