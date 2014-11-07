from random import random

def frange(x0, x1, jump):
    while x0 < x1:
        yield x0
        x0 += jump

def frandrange(fmin, fmax):
    return fmin + (fmax-fmin)*random()
