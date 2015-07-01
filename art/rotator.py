__author__ = 'rafe'

import time


class Art(object):

    description = "Arts Rotator"

    def __init__(self, matrix, config):
        self.__timeout = config.get('TIMEOUT', 30)  # defaults to 30 seconds.
        self.__selector = config.get('SELECTOR', lambda: None)

    @property
    def selected(self):
        return self[self.__selection][1]

    def select(self, index):
        self[index]  # Check index
        self.__selection = index

    def start(self, matrix):
        self.__last_flip = time.time()

    def refresh(self, matrix):
        elapsed = time.time() - self.__last_flip
        print elapsed, self.__timeout
        if elapsed >= self.__timeout:
            self.__selector()
            self.__last_flip = time.time()
            print self.__selector()
            self.__selector(self.__selector() + 1)

    def interval(self):
        return 30
