class HQ(object):

    """
    use the HQ class to savely wrap art init blocks when you need to
    switch on HQ for set-up purposes. For example:

        from opc.matrix import HQ


        class Art(object):

            def __init__(self, matrix):

                with HQ(matrix):
                    initialization stuff...
    """

    def __init__(self, matrix):
        self.matrix = matrix

    def __enter__(self):
        self.matrix.hq()

    def __exit__(self, type, value, traceback):
        self.matrix.hq(False)
