__author__ = 'rafe'

import time

from art import compound


class Art(compound.Art):

    description = "Arts Rotator"

    def __init__(self, matrix, config):
        super(Art, self).__init__(matrix, config)
        self.__timeout = config.get('TIMEOUT', 30)  # defaults to 30 seconds.
        self.__selected = 0

    @property
    def selected(self):
        if len(self):
            return self[self.__selected][1]
        else:
            return None

    def start(self, matrix):
        matrix.clear()
        self.__last_flip = time.time()
        super(Art, self).start(matrix)

    def refresh(self, matrix):
        now = time.time()
        elapsed = now - self.__last_flip
        if elapsed >= self.__timeout:
            self.__selected = (self.__selected + 1) % len(self)
            matrix.clear()
            self.selected.start(matrix)
            self.__last_flip = now
        if self.selected:
            self.selected.refresh(matrix)
        else:
            matrix.clear()

    def interval(self):
        return 30
