#encoding: utf-8

import curses
import logging
import numpy as np

from error import TtyTooSmall
from utils.prof import timefunc


def initCurses():
    global stdscr

    stdscr = curses.initscr()
    curses.start_color()


def exitCurses():
    curses.endwin()


class AnsiClient:
    """
    Simple text based client that displays a LED string as asciiart. There
    are several ways to do this, depending on the capability level of the
    terminal. See the specific implementations for details.

    TODO: add support for xterm-256
    """

    MAP10 = " .-=:+*#%@"    # ten step asciiart gradient
    MAP9 = u" ⡀⢂⢌⢕⡫⢷⣽⣿"     # nine step braille gradient, but
                            # don't even bother before python 3.3
                            # and libncursesw.so.5

    def __init__(self, width, height, address, chars=None):
        self.width = width
        self.height = height

        initCurses()
        stdscr.clear()

        if chars == None:
            chars = self.MAP10

        self.chars = dict(enumerate(chars))

        COLOR_WHITE = 0  # curses has white locked in postition 0
        COLOR_BLACK = 1
        COLOR_RED = 2
        COLOR_GREEN = 3
        COLOR_YELLOW = 4
        COLOR_BLUE = 5
        COLOR_MAGENTA = 6
        COLOR_CYAN = 7

        self.colors = {
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

    @timefunc
    def _addstr(self, pixel):
        stdscr.addstr(self.chars[pixel[0]], pixel[1])

    @timefunc
    def _char(self, pixels):
        return (np.sum(pixels, axis=2) / 85).astype(dtype=np.uint8)  

    @timefunc
    def _colorindex(self, pixels):
        return np.char.mod('%c', np.ceil(pixels/128).astype(dtype=np.uint8)+48)

    @timefunc
    def _color(self, indices):
        shape = indices.shape
        reshaped = indices.reshape(shape[0]*shape[1], shape[2])
        pixels = [self.colors["".join(pixel)] for pixel in reshaped]

        return np.asarray(pixels).reshape(shape[0], shape[1])

    @timefunc
    def _show(self, pixels):
        stdscr.addstr(0, 0, " + " + "-"*self.width + " +\n")

        """
          - sum the set on axis 2, then divide the result by 85. This'll
            give a value in range where we can look up the ascii art shade.
            85 is 256/3, and allows us to squish three 8-bit values into one.
          - map value to ascii art symbol

          - divide each value so that each gun is in range 0..2, with zero
            being off, 1-127 = 1, 128-255 = 2 (divide by 128, round up)
          - convert the resultant (r, g, b) tuple into a string
          - map the resultant string to a curses color

          - combine the two result sets on a per pixel basis

          - draw it!
        """

        char = self._char(pixels)
        color = self._color(self._colorindex(pixels))

        encoded = np.dstack((char, color))
        for row in np.rot90(encoded):
            stdscr.addstr(" | ")
            for pixel in row:
                self._addstr(pixel)
            stdscr.addstr(" |\n")

        stdscr.addstr(" + " + "-"*self.width + " +\n")
        stdscr.refresh()

    def show(self, pixels):
        try:
            self._show(pixels)
        except curses.error as e:
            ttyheight, ttywidth = stdscr.getmaxyx()
            message = (
                "Your screen (%d, %d) is too small to support this size"
                " matrix (%d, %d)" % (ttywidth, ttyheight, self.width, self.height)
                )

            raise TtyTooSmall(message)

    def terminate(self):
        exitCurses()
