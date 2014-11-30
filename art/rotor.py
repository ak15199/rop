from opc.hue import hsvToRgb

from math import sin, cos, fmod, pi


class Art(object):

    description = "Radar-like, but without the enemy planes"

    def __init__(self, matrix):
        self.angle = 0.0
        self.hue = 0
        self.astep = pi/48
        self.hstep = pi/1024

        self.radius = min(matrix.width, matrix.height)/2.2
        self.x0 = matrix.width/2
        self.y0 = matrix.height/2

    def start(self, matrix):
        matrix.clear()

    def refresh(self, matrix):
        matrix.fade(0.995)

        y0 = matrix.height/2
        x0 = matrix.width/2

        if self.angle >= pi:
            x0 -= 1

        if self.angle > (0.5*pi) and self.angle < (1.5*pi):
            y0 -= 1

        x1 = int(self.x0 + self.radius * sin(self.angle-self.astep))
        y1 = int(self.y0 + self.radius * cos(self.angle+self.astep))

        x2 = int(self.x0 + self.radius * sin(self.angle))
        y2 = int(self.y0 + self.radius * cos(self.angle))

        matrix.drawPoly(
            [(self.x0, self.y0), (x1, y1), (x2, y2)],
            hsvToRgb(self.hue)
        )

        self.hue = fmod(self.hue+self.hstep, 1.0)
        self.angle += self.astep

    def interval(self):
        return 60
