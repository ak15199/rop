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
    curses.use_default_colors()


def exitCurses():
    curses.endwin()


class AnsiClient:
    """
    Simple text based client that displays a LED string as asciiart. There
    are several ways to do this, depending on the capability level of the
    terminal. See the specific implementations for details.

    TODO: add support for xterm-256
    """

    MAP10 = " .-:=+*#%@"    # ten step asciiart gradient
    MAP9 = u" ⡀⢂⢌⢕⡫⢷⣽⣿"     # nine step braille gradient, but
                            # don't even bother before python 3.3
                            # and libncursesw.so.5

    def __init__(self, server=None):
        initCurses()
        stdscr.clear()

        self.chars = dict(enumerate(self.MAP10))

        COLOR_WHITE = 0  # curses has white locked in postition 0
        COLOR_BLACK = 1
        COLOR_RED = 2
        COLOR_GREEN = 3
        COLOR_YELLOW = 4
        COLOR_BLUE = 5
        COLOR_MAGENTA = 6
        COLOR_CYAN = 7

        self.colors = [
            curses.color_pair(COLOR_BLACK),
            curses.color_pair(COLOR_BLUE),
            curses.color_pair(COLOR_BLUE)+curses.A_BOLD,
            curses.color_pair(COLOR_GREEN),
            curses.color_pair(COLOR_CYAN),
            curses.color_pair(COLOR_CYAN),                   # approx
            curses.color_pair(COLOR_GREEN)+curses.A_BOLD,
            curses.color_pair(COLOR_CYAN),                   # approx
            curses.color_pair(COLOR_CYAN)+curses.A_BOLD,
            curses.color_pair(COLOR_RED),
            curses.color_pair(COLOR_MAGENTA),
            curses.color_pair(COLOR_MAGENTA),                # approx
            curses.color_pair(COLOR_YELLOW),
            curses.color_pair(COLOR_WHITE),
            curses.color_pair(COLOR_BLUE)+curses.A_BOLD,     # approx
            curses.color_pair(COLOR_YELLOW),                 # approx
            curses.color_pair(COLOR_GREEN)+curses.A_BOLD,    # approx
            curses.color_pair(COLOR_CYAN)+curses.A_BOLD,     # approx
            curses.color_pair(COLOR_RED)+curses.A_BOLD,
            curses.color_pair(COLOR_RED)+curses.A_BOLD,      # approx
            curses.color_pair(COLOR_MAGENTA)+curses.A_BOLD,
            curses.color_pair(COLOR_YELLOW),                 # approx
            curses.color_pair(COLOR_RED)+curses.A_BOLD,      # approx
            curses.color_pair(COLOR_MAGENTA)+curses.A_BOLD,  # approx
            curses.color_pair(COLOR_YELLOW)+curses.A_BOLD,
            curses.color_pair(COLOR_YELLOW)+curses.A_BOLD,   # approx
            curses.color_pair(COLOR_WHITE)+curses.A_BOLD,
        ]

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

        if curses.COLORS == 256:
            self.c_mod = 6
            for index in range(216):
                curses.init_pair(index, -1, index + 16)
        else:
            self.c_mod = 3
            for index in range(1, 8):
                curses.init_pair(index, color[index], curses.COLOR_BLACK)

    def setGeometry(self, width, height):
        self.width = width
        self.height = height

    @timefunc
    def _addstr(self, pixel):
        if curses.COLORS == 256:
            stdscr.addstr(' ', curses.color_pair(pixel[1]))
        else:
            stdscr.addstr(self.chars[pixel[0]], self.colors[pixel[1]])

    @timefunc
    def _char(self, pixels):
        return (np.sum(pixels, axis=2) / 85).astype(dtype=np.uint8)  

    @timefunc
    def _colorindex(self, pixels):
        return np.ceil(np.dot(pixels, (self.c_mod - 1)) / 256)

    @timefunc
    def _color(self, indices):
        shape = indices.shape
        reshaped = indices.reshape(shape[0]*shape[1], shape[2])
        pixels = [int(sum(self.c_mod ** (2 - i) * v
                          for i,v in enumerate(pixel)))
                  for pixel in reshaped]

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

    def putPixels(self, channel, pixels):
        try:
            self._show(pixels)
        except curses.error as e:
            ttyheight, ttywidth = stdscr.getmaxyx()
            message = (
                "Your screen (%d, %d) is too small to support this size"
                " matrix (%d, %d)" % (ttywidth, ttyheight, self.width, self.height)
                )

            raise TtyTooSmall(message)

    def sysEx(self, systemId, commandId, msg):
        pass

    def setGlobalColorCorrection(self, gamma, r, g, b):
        pass

    def terminate(self):
        exitCurses()
