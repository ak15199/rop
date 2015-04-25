class ArtBaseClass(object):
    """
    Your art should inherit from this. As a minimum, you should implement the
    constructor and refresh methods. Interval is implemented as a method rather
    than a property because some arts may want to vary their refresh speed.
    """

    description = "Art description goes here"

    def __init__(self, matrix, config):
        raise NotImplementedError

    def start(self, matrix):
        pass

    def refresh(self, matrix):
        raise NotImplementedError

    def interval(self):
        return 400
