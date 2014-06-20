#from dict import iteritems


class Ansi_1:
    MAP10 = " .:-=+*#%@"

    def _shortAnsi(self, v):
        return self.MAP10[min(9,max(v,0))]

    def convert(self, color):
        total = 0
        for v in color:
            total = v + 1.1*total

        total /= 100

        return self._shortAnsi(int(total))

class AnsiClient:
    """
    Simple text based client that displays a LED
    string as asciiart.

    TODO: A more advanced version would use the xterm-256
            color set, although not all terminal emulators
            support this
    """

    def __init__(self, width, height, zigzag):
        self.width = width
        self.height = height
        self.zigzag = zigzag

        self.converter = Ansi_1()

    def show(self, pixels):
        print '\033[1;1H\033[J'
        print " + " + "-"*self.width + " +"

        for y in range(self.height):
            if self.zigzag and (y&1):
                start, stop, step = self.width-1, -1, -1
            else:
                start, stop, step = 0, self.width, 1

            row = [ self.converter.convert(pixels[x+y*self.height]) for x in range(start, stop, step) ]

            print ' | ' + ''.join(row) + ' |'

        print " + " + "-"*self.width + " +"
        
