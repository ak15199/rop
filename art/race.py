import logging
from math import sin, cos, pi
from opc.hue import getColorGen
from utils.frange import frange


class Polar(object):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.phase = 0
        self.radius = radius

    def transform(self, angle):
        x = self.x + self.radius * sin(angle)
        y = self.y + self.radius * cos(angle)

        return x, y


class Racer(object):

    def __init__(self, x, y, position, accel):
        self.polar = Polar(x, y, position)
        self.accel = accel

    def next(self, theta):
        angle = self.accel * sin(theta)

        return self.polar.transform(angle)


class Art(object):

    description = "Racing pixels"

    def __init__(self, matrix):
        self.hue = getColorGen(0.001)
        self.clock = 0
        self.racers = []
        xmax = matrix.midWidth-1
        for x in frange(0, xmax, .5):
            offset = pi*(0.2 + 0.6 * x/xmax)
            accel = 20 * sin(offset)
            racer = Racer(matrix.midWidth, matrix.midHeight, x, accel)
            self.racers.append(racer)

    def start(self, matrix):
        matrix.clear()
        matrix.setFirmwareConfig(nointerp=True)

    def refresh(self, matrix):
        matrix.shift(.9, .9, .9)

        hue = self.hue.next()
        for racer in self.racers:
           x, y = racer.next(self.clock)
           matrix.drawPixel(x, y, hue)

        self.clock += 0.01

    def interval(self):
        return 100
