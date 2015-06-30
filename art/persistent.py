__author__ = 'rafe'

import compound
from opc import buffer


class Art(compound.Art):

    description = "Persistent"

    def start(self, matrix):
        self.__persistent = type(matrix)(matrix.width, matrix.height, None)
        super(Art, self).start(matrix)

    def refresh(self, matrix):
        super(Art, self).refresh(self.__persistent)
        matrix.copy(self.__persistent, 0, 0)

