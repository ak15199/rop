from matrix import OPCMatrix

typeface_bbc = {
    "geometry": { "width": 8, "height": 8},
    "bitmaps": [

        0x00000000, 0x00000000, 0x18181818, 0x18001800,	  #   !
        0x6c6c6c00, 0x00000000, 0x36367f36, 0x7f363600,	  # " #
        0x0c3f683e, 0x0b7e1800, 0x60660c18, 0x30660600,	  # $ %
        0x386c6c38, 0x6d663b00, 0x0c183000, 0x00000000,	  # & '
        0x0c183030, 0x30180c00, 0x30180c0c, 0x0c183000,	  # ( )
        0x00187e3c, 0x7e180000, 0x0018187e, 0x18180000,	  # * +
        0x00000000, 0x00181830, 0x0000007e, 0x00000000,	  # , -
        0x00000000, 0x00181800, 0x00060c18, 0x30600000,	  # . /
        0x3c666e7e, 0x76663c00, 0x18381818, 0x18187e00,	  # 0 1
        0x3c66060c, 0x18307e00, 0x3c66061c, 0x06663c00,	  # 2 3
        0x0c1c3c6c, 0x7e0c0c00, 0x7e607c06, 0x06663c00,	  # 4 5
        0x1c30607c, 0x66663c00, 0x7e060c18, 0x30303000,	  # 6 7
        0x3c66663c, 0x66663c00, 0x3c66663e, 0x060c3800,	  # 8 9
        0x00001818, 0x00181800, 0x00001818, 0x00181830,	  # : ;
        0x0c183060, 0x30180c00, 0x00007e00, 0x7e000000,	  # < =
        0x30180c06, 0x0c183000, 0x3c660c18, 0x18001800,	  # > ?
        0x3c666e6a, 0x6e603c00, 0x3c66667e, 0x66666600,	  # @ A
        0x7c66667c, 0x66667c00, 0x3c666060, 0x60663c00,	  # B C
        0x786c6666, 0x666c7800, 0x7e60607c, 0x60607e00,	  # D E
        0x7e60607c, 0x60606000, 0x3c66606e, 0x66663c00,	  # F G
        0x6666667e, 0x66666600, 0x7e181818, 0x18187e00,	  # H I
        0x3e0c0c0c, 0x0c6c3800, 0x666c7870, 0x786c6600,	  # J K
        0x60606060, 0x60607e00, 0x63777f6b, 0x6b636300,	  # L M
        0x6666767e, 0x6e666600, 0x3c666666, 0x66663c00,	  # N O
        0x7c66667c, 0x60606000, 0x3c666666, 0x6a6c3600,	  # P Q
        0x7c66667c, 0x6c666600, 0x3c66603c, 0x06663c00,	  # R S
        0x7e181818, 0x18181800, 0x66666666, 0x66663c00,	  # T U
        0x66666666, 0x663c1800, 0x63636b6b, 0x7f776300,	  # V W
        0x66663c18, 0x3c666600, 0x6666663c, 0x18181800,	  # X Y
        0x7e060c18, 0x30607e00, 0x7c606060, 0x60607c00,	  # Z [
        0x00603018, 0x0c060000, 0x3e060606, 0x06063e00,	  # \ ]
        0x183c6642, 0x00000000, 0x00000000, 0x000000ff,	  # ^ _
        0x1c36307c, 0x30307e00, 0x00003c06, 0x3e663e00,	  # ` a
        0x60607c66, 0x66667c00, 0x00003c66, 0x60663c00,	  # b c
        0x06063e66, 0x66663e00, 0x00003c66, 0x7e603c00,	  # d e
        0x1c30307c, 0x30303000, 0x00003e66, 0x663e063c,	  # f g
        0x60607c66, 0x66666600, 0x18003818, 0x18183c00,	  # h i
        0x18003818, 0x18181870, 0x6060666c, 0x786c6600,	  # j k
        0x38181818, 0x18183c00, 0x0000367f, 0x6b6b6300,	  # l m
        0x00007c66, 0x66666600, 0x00003c66, 0x66663c00,	  # n o
        0x00007c66, 0x667c6060, 0x00003e66, 0x663e0607,	  # p q
        0x00006c76, 0x60606000, 0x00003e60, 0x3c067c00,	  # r s
        0x30307c30, 0x30301c00, 0x00006666, 0x66663e00,	  # t u
        0x00006666, 0x663c1800, 0x0000636b, 0x6b7f3600,	  # v w
        0x0000663c, 0x183c6600, 0x00006666, 0x663e063c,	  # x y
        0x00007e0c, 0x18307e00, 0x0c181870, 0x18180c00,	  # z {
        0x18181800, 0x18181800, 0x3018180e, 0x18183000,	  # | }

    ],
}

class OPCText:
    """
    This implementation assumes an 8x8 pixel grid per character, with one
    byte per row.
    """

    def __init__(self, typeface):
        self.typeface = typeface

    def drawHalfLetter(self, matrix, x, y, letter, offset, fg, bg):
        word = self.typeface["bitmaps"][2*letter+offset]
        ybase = y + 4*(offset)
        for window in reversed(range(4)):
            byte = word & 0xff
            word = word >> 8
            for bit in reversed(range(8)):
                if byte & 1 == 1:
                    matrix.drawPixel(x+bit, ybase + window, fg)
                else:
                    matrix.drawPixel(x+bit, ybase + window, bg)

                byte = byte >> 1

    def drawLetter(self, matrix, x, y, char, fg, bg):
        letter = ord(char) - 32 # printable ASCII starts at index 32
        self.drawHalfLetter(matrix, x, y, letter, 0, fg, bg)
        self.drawHalfLetter(matrix, x, y, letter, 1, fg, bg)

    def drawText(self, matrix, x, y, string, fg, bg):
        offset = 0
        for char in list(string):
            xpos = x+offset
            if xpos>=-7:
                if xpos-7<matrix.width():
                    self.drawLetter(matrix, xpos, y, char, fg, bg)
                else:
                    return None

            offset += 8

        return xpos + 8
