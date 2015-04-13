from random import random


def frange(x0, x1, jump):
    while x0 < x1:
        yield x0
        x0 += jump
