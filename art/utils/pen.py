from opc.colors import *
from opc.matrix import OPCMatrix
from opc.hue import hsvToRgb

from random import random, randrange
from math import fmod, sin, cos

HUEDELTA = 0.0005

class Pen:
    def __init__(self, width, height, x, y, dx=1, dy=1, persist=True):
        self.hue = random()
        self.value = 1
        self.x, self.x0 = x, x
        self.y, self.y0 = y, y
        self.w = width
        self.h = height
        self.dx = dx
        self.dy = dy
        self.ax = self.trap
        self.ay = self.trap
        self.persist = persist
        self.angle = 0
        self.theta = 0.01


    def setValue(self, value):
        self.value = value

    def setBumpStrategy(self, func, x=False, y=False):
        if x: self.ax = func
        if y: self.ay = func

    def trap(self, x=False, y=False):
        raise Exception("Bump strategy not set (%d, %d)"%(x, y))

    def randomreset(self, x=False, y=False):
        if x: self.x = self.x0
        if y: self.y = self.y0
        if not x: self.x = randrange(self.w)
        if not y: self.y = randrange(self.h)

    def reverse(self, x=False, y=False):
        if x: self.dx = -self.dx 
        if y: self.dy = -self.dy 

    def random(self, x=False, y=False):
        if x: self.x = randrange(self.w)
        if y: self.y = randrange(self.h)

    def none(self, x=False, y=False):
        pass

    def clock(self, matrix):
        if self.theta:
            self.angle += self.theta
            mx, my = sin(self.angle), cos(self.angle)
        else:
            mx, my = 1, 1

        if not self.persist:
            matrix.drawPixel(self.x, self.y, BLACK)

        self.x += self.dx
        if (self.x < 1 and self.dx < 0) or (self.x >= self.h-1 and self.dx > 0):
            self.ax(x=True)
        
        self.y += self.dy
        if (self.y < 1 and self.dy < 0) or (self.y >= self.w-1 and self.dy > 0):
            self.ay(y=True)
        
        matrix.drawPixel(self.x, self.y, hsvToRgb(self.hue, v=self.value))
        self.hue = fmod(self.hue + HUEDELTA, 1)
