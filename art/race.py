import logging
from math import sin, cos, pi
from opc.hue import getHueGen
from utils.frange import frange


class Racer(object):

    def __init__(self, x, y, radius, phase):
        self.x = x
        self.y = y
        self.phase = phase
        self.radius = radius

    def next(self, clock):
        angle = pi * (1 + sin(self.phase * clock))
        x = self.x + self.radius * sin(angle)
        y = self.y + self.radius * cos(angle)

        return x, y


class Art(object):

    description = "Racing pixels"

    def __init__(self, matrix):
        self.hue = getHueGen(0.001)
        self.clock = 0
        self.racers = []
        xmax = matrix.midWidth-1
        for x in frange(0, xmax, .5):
            offset = pi*(x/xmax)
            phase = 1 + .1 * sin(offset)
            racer = Racer(matrix.midWidth, matrix.midHeight, x, phase)
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
        self.clock += 0.05

    def interval(self):
        return 100
