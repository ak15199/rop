from basecls.flow import Flow

class Art(Flow):

    def __init__(self, matrix):
        Flow.__init__(self, matrix, True)
