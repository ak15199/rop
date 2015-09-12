__author__ = 'rafe'


class Art(object):

    description = "Fade"

    def __init__(self, matrix, config):
        self.__amount = config.get('FADE', 0.7)

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        matrix.fade(self.__amount)

    def interval(self):
        return 30
