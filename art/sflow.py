from baseclasses.flow import Flow


class Art(Flow):

    description = "Like cflow, but color blocks are segmented"

    def __init__(self, matrix):
        Flow.__init__(self, matrix, False)
