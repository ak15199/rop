__author__ = 'rafe'

from opc import nphue
import numpy as np


class Art(object):

    description = "Color Rotation"

    def __init__(self, matrix, config):
        self.dh = config.get('dh', 1.0)
        self.ds = config.get('ds', 1.0)
        self.dv = config.get('dv', 1.0)

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        matrix.shift(dh=self.dh, ds=self.ds, dv=self.dv)

    def interval(self):
        return 30
