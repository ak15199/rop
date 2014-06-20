#from dict import iteritems

MAP10 = " .:-=+*#%@"

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

    def _shortAnsi(self, v):
        return MAP10[min(9,max(v,0))]

    def _rgb2ansi(self, color):
        total = 0
        for v in color:
            total = v + 1.1*total

        total /= 100

        return self._shortAnsi(int(total))

    def show(self, pixels):
        print '\033[1;1H\033[J'
        print " + " + "-"*self.width + " +"

        for y in range(self.height):
            if self.zigzag and (y&1):
                start, stop, step = self.width-1, -1, -1
            else:
                start, stop, step = 0, self.width, 1

            row = [ self._rgb2ansi(pixels[x+y*self.height]) for x in range(start, stop, step) ]

            print ' | ' + ''.join(row) + ' |'

        print " + " + "-"*self.width + " +"
        
