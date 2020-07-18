from ..colors import BLACK

class Transform(object):

    def rotate(self, angle):
        """Rotate the buffer by the given angle"""
        self.buf.rotate(angle)

    def flip(self, ud=None, lr=None):
        """Flip the buffer in one or both axes"""
        self.buf.flip(ud, lr)

    def paste(self, source, mask):
        """Paste the masked part of the source buf into our buf"""
        self.buf.paste(source.buf, mask.buf)

    def add(self, source):
        """Update the matrix with non-black pixels from the source"""
        self.buf.add(source.buf)

    def clear(self, color=BLACK):
        """
        Wipe the matrix to any color, defaulting to black.
        """
        self.buf.clear(color)

    def scroll(self, direction):
        """Scroll the matrix in the given direction (left, right, up, down)"""
        self.buf.scroll(direction)
