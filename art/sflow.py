from .baseclasses.flow import Flow


class Art(Flow):

    description = "Like cflow, but color blocks are segmented"

    def __init__(self, matrix, config):
        Flow.__init__(self, matrix, config)

        self.contiguous = False
