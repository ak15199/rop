from opc.hue import hsvToRgb
from opc.matrix import OPCMatrix

from random import random
from math import sin, pi

class Flow:

    huecount=(8+1) # the addition covers offscreen for recoloring

    def __init__(self, matrix, contiguous):
        numpix = matrix.numpix()
        self.base=0
        self.offset=0
        self.contiguous=contiguous
        self.usecount=[]
        self.blocksize=numpix/(self.huecount-1)
  
        self.hues=[]
        for hue in range(0,self.huecount):
            self.hues.append(random())

        self.sinlut=[]
        for i in range(0,self.blocksize):
            s=sin(pi*i/(self.blocksize-1))
            self.sinlut.append(s*s*s)

    def start(self, matrix):
        pass

    def _color(self):
        self.offset+=1

        if self.contiguous:
            hue = 0.0 + (self.offset+2*self.base)%256
            return hsvToRgb(hue/255)

        index = ((self.base+self.offset)/self.blocksize) % self.huecount
        hue = self.hues[index]

        phase = (self.base+self.offset)%self.blocksize
        value = self.sinlut[phase]

        ++self.usecount[index]

        return hsvToRgb(hue, 1, value)

    def plot(self, matrix, x, y):
        color=self._color()
        if color == (255, 255, 255):
            print "art %d, %d" % (x,y)
        matrix.drawPixel(x, y, color)

    def refresh(self, matrix):
        xmin=0
        ymin=0
        xmax=matrix.width()
        ymax=matrix.height()
        x=xmax-1
        y=0
        index=self.offset
  
        self.offset=0
        self.base+=1
  
        self.usecount = [0]*self.huecount
 
        while xmin<xmax and ymin<ymax:
            while x<xmax-1:
                self.plot(matrix, x, y)
                x=x+1
      
            xmax-=1

            while y<ymax-1:
                self.plot(matrix, x, y)
                y=y+1
      
            ymax-=1

            while x>xmin:
                self.plot(matrix, x, y)
                x=x-1
          
            xmin+=1

            while y>ymin:
                self.plot(matrix, x, y)
                y=y-1
      
            ymin+=1
  
        self.plot(matrix, x, y)
 
        for i in range(0,self.huecount):
            if self.usecount[i]==1:
                self.hues[i]=random()
  
    def interval(self):
        return 700

