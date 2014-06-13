from opc.colors import *
from opc.matrix import OPCMatrix
from opc.hue import getHueGen

from math import sin, cos, pi, fabs
from utils.frange import frange

DELTA_Z = 0.05

class Art:

    def __init__(self, matrix):
        self.hue = getHueGen(0.01)
        self.phase_z = 0

    def start(self, matrix):
        matrix.clear()

    def refresh(self, matrix):
        matrix.shift(.9, 1, .9)
        self.phase_z += DELTA_Z

        color = self.hue.next()
        center = matrix.width()/2
        theta = sin(self.phase_z)
        if theta < 0:
            theta_x, theta_y = 1, 1 - 2*theta
        else:
            theta_x, theta_y = 1 + 2*theta, 1

        for angle in frange(0, 2*pi, 0.01):
            x = center + center * sin(theta_x * angle)
            y = center + center * cos(theta_y * angle)
            matrix.drawPixel(x, y, color)
        
    def interval(self):
        return 100

