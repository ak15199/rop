class Art(object):

    description = "A silly boring chess board"

    GRIDSIZE = 8

    def __init__(self, matrix):
        pass

    def start(self, matrix):
        matrix.clear((96, 64, 24))

        xcorner = matrix.width/2 - (self.GRIDSIZE/2)
        ycorner = matrix.height/2 - (self.GRIDSIZE/2)

        matrix.drawRect(xcorner-1, ycorner-1,
                        self.GRIDSIZE+1, self.GRIDSIZE+1, (128, 128, 128))

        for x in range(self.GRIDSIZE):
            for y in range(self.GRIDSIZE):
                black = (x & 1) ^ (y & 1)
                if black:
                    color = (192, 0, 0)
                else:
                    color = (0, 0, 192)

                matrix.drawPixel(xcorner+x, ycorner+y, color)

        matrix.show()

    def refresh(self, matrix):
        pass

    def interval(self):
        return 400
