from opc.hue import getColorGen

from math import sin, cos, pi
from utils.frange import frange

import logging

DELTA_Z = 0.02


class Art(object):

    description = "Lissajous figures"

    def __init__(self, matrix):
        self.color = getColorGen(0.01)
        self.phase_z = 0

    def start(self, matrix):
        matrix.clear()

    def refresh(self, matrix):
        matrix.shift(.9, 1, .9)
        self.phase_z += DELTA_Z

        color = self.color.next()
        xcenter = matrix.width/2.0
        ycenter = matrix.height/2.0
        theta = sin(self.phase_z)
        if theta < 0:
            theta_x, theta_y = 1, 1 - 2*theta
        else:
            theta_x, theta_y = 1 + 2*theta, 1

        count = 0
        step = 2*pi / (matrix.numpix/6)
        for angle in frange(0, 2*pi, step):
            x = int(xcenter + xcenter * sin(theta_x * angle))
            y = int(ycenter + ycenter * cos(theta_y * angle))
            if count == 0:
                matrix.setCursor((x, y))
            elif matrix.movesCursor(x, y):
                matrix.drawLineRelative(x, y, color)

            count += 1

    def interval(self):
        return 150
