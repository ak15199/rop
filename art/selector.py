__author__ = 'rafe'

import compound


class Art(compound.Art):

    description = "Selector"

    def __init__(self, matrix, config):
        super(Art, self).__init__(matrix, config)
        self.__selector = config.get('SELECTOR', lambda: 0)
        self.__selection = None

    @property
    def selected(self):
        return self[self.__selection][1]

    def select(self, index):
        self[index]  # Check index
        self.__selection = index

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        selection = self.__selector() % len(self)
        if selection != self.__selection:
            self.select(selection)
            self.selected.start(matrix)
        self.selected.refresh(matrix)

    def interval(self):
        return self.selected.interval()
