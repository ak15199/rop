from opc.matrix import OPCMatrix

"""
This is a sample template that will duck type successfully
Make sure that your art has implementations for these.
"""
class Art(object):

    description = "Your description goes right here"

    def __init__(self, matrix):
        pass

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        pass
  
    def interval(self):
        return 400

