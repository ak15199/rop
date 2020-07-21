from __future__ import division

import curses
import numpy as np

from opc.drivers.baseclass import RopDriver
from opc.error import TtyTooSmall
from opc.utils.prof import timefunc


window = None  # for flake8


def initCurses(width, height):
    global window

    curses.initscr()
    window = curses.newwin(2+height, 4+2*width, 1, 1)
    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(0)

    window.clear()
    window.border(0)


def exitCurses():
    curses.nocbreak()
    window.keypad(False)
    curses.echo()
    curses.endwin()


class Driver(RopDriver):
    """
    Simple text based client that displays a LED string as asciiart. There
    are several ways to do this, depending on the capability level of the
    terminal. See the specific implementations for details.
    """

    MAP10 = " .-:=+*#%@"    # ten step asciiart gradient

    def __init__(self, width, height, address):
        global window

        self.width = width
        self.height = height

        initCurses(width, height)

        if curses.COLORS == 256:
            # initialize colors as the background, render spaces.
            for index in range(216):
                curses.init_pair(index, -1, index + 16)
            self.chars = " " * 10

            self.c_mod = 6
            self.colors = [curses.color_pair(i) for i in range(216)]
        else:
            for index in range(8):
                curses.init_pair(index, index, -1)

            self.chars = self.MAP10
            self.c_mod = 3
            self.colors = [
                # lines that end 'ax' are approximations
                curses.color_pair(curses.COLOR_BLACK),
                curses.color_pair(curses.COLOR_BLUE),
                curses.color_pair(curses.COLOR_BLUE)+curses.A_BOLD,
                curses.color_pair(curses.COLOR_GREEN),
                curses.color_pair(curses.COLOR_CYAN),
                curses.color_pair(curses.COLOR_CYAN),                   # ax
                curses.color_pair(curses.COLOR_GREEN)+curses.A_BOLD,
                curses.color_pair(curses.COLOR_CYAN),                   # ax
                curses.color_pair(curses.COLOR_CYAN)+curses.A_BOLD,
                curses.color_pair(curses.COLOR_RED),
                curses.color_pair(curses.COLOR_MAGENTA),
                curses.color_pair(curses.COLOR_MAGENTA),                # ax
                curses.color_pair(curses.COLOR_YELLOW),
                curses.color_pair(curses.COLOR_WHITE),
                curses.color_pair(curses.COLOR_BLUE)+curses.A_BOLD,     # ax
                curses.color_pair(curses.COLOR_YELLOW),                 # ax
                curses.color_pair(curses.COLOR_GREEN)+curses.A_BOLD,    # ax
                curses.color_pair(curses.COLOR_CYAN)+curses.A_BOLD,     # ax
                curses.color_pair(curses.COLOR_RED)+curses.A_BOLD,
                curses.color_pair(curses.COLOR_RED)+curses.A_BOLD,      # ax
                curses.color_pair(curses.COLOR_MAGENTA)+curses.A_BOLD,
                curses.color_pair(curses.COLOR_YELLOW),                 # ax
                curses.color_pair(curses.COLOR_RED)+curses.A_BOLD,      # ax
                curses.color_pair(curses.COLOR_MAGENTA)+curses.A_BOLD,  # ax
                curses.color_pair(curses.COLOR_YELLOW)+curses.A_BOLD,
                curses.color_pair(curses.COLOR_YELLOW)+curses.A_BOLD,   # ax
                curses.color_pair(curses.COLOR_WHITE)+curses.A_BOLD,
            ]

    @timefunc
    def _addstr(self, pixel):
        global window

        window.addstr(self.chars[pixel[0]]*2, self.colors[pixel[1]])

    @timefunc
    def _char(self, pixels):
        return (np.sum(pixels, axis=2) / 85).astype(dtype=np.uint8)

    @timefunc
    def _colorindex(self, pixels):
        # map 0 - 256 to  0 - c_mod
        return np.round(pixels / (256 / (self.c_mod - 1)))

    @timefunc
    def _color(self, pixels):
        return np.sum(pixels * np.power(self.c_mod, [2, 1, 0]), axis=2,
                      dtype=np.int16)

    @timefunc
    def _show(self, pixels):
        global window


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

        y = 0
        encoded = np.dstack((char, color))
        for row in np.rot90(encoded):
            y += 1
            window.move(y, 2)
            for pixel in row:
                self._addstr(pixel)

        window.refresh()

    def putPixels(self, channel, pixels):
        try:
            self._show(pixels)
        except curses.error as e:
            ttyheight, ttywidth = window.getmaxyx()
            message = (
                '--'+str(e)+"-- Your screen (%d, %d) is too small to support this size"
                " matrix (%d, %d)" %
                (ttywidth, ttyheight, self.width, self.height)
                )

            raise TtyTooSmall(message)

    def setFirmwareConfig(self, nodither=False, nointerp=False,
                          manualled=False, ledonoff=True):
        pass

    def setGlobalColorCorrection(self, gamma, r, g, b):
        pass

    def terminate(self):
        exitCurses()
