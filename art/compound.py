__author__ = 'rafe'

import importer


class Art(object):

    description = "Compound"

    def __init__(self, matrix, config):
        self.__arts = []
        for name, sub_config in config.get('COMPOUND', []):
            art = importer.ImportPlugins('art', [], [name + '.py'], None, matrix, sub_config)
            if not art:
                raise Exception('Could not find art %s' % (name,))
            self.__arts.append((name, art.get(name)))

    def start(self, matrix):
        for _, art in self.__arts:
            art.start(matrix)

    def refresh(self, matrix):
        for _, art in self.__arts:
            art.refresh(matrix)

    def interval(self):
        return 30
