from ..utils.prof import timefunc


class Cursor(object):

    @timefunc
    def setCursor(self, pos=(0, 0)):
        """
        Set the cursor position. This is used by draw relative operations
        """
        x, y = pos
        self.cursor = (x, y)

    @timefunc
    def movesCursor(self, x, y):
        return self.cursor[0] != x or self.cursor[1] != y

    @timefunc
    def getCursor(self):
        """
        Get the current cursor position
        """
        return self.cursor
