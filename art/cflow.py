from baseclasses.flow import Flow


class Art(Flow):

    description = "Spiral flow from middle to edge with continuous color"

    def __init__(self, matrix):
        Flow.__init__(self, matrix, True)
