from _baseclass import ArtBaseClass

from opc.colors import *
from opc.matrix import OPCMatrix

"""
This is a sample template that will duck type successfully
Make sure that your art has implementations for these.
"""
class Art(ArtBaseClass):

    description = "Your description goes right here"

    def __init__(self, matrix):
        pass

    def start(self, matrix):
        matrix.drawLine(2,2,20,20,WHITE)
        matrix.drawLine(2,2,20,2,WHITE)
        matrix.soften()

    def refresh(self, matrix):
        pass
  
    def interval(self):
        return 400

