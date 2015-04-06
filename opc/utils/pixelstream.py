import numpy as np


def process(buf, func, *args):
    #XXX: experimental
    #f = np.vectorize(func, otypes=[np.float])
    #return f(buf)

    shape = buf.shape
    reshaped = buf.reshape(shape[0]*shape[1], shape[2])

    pixels = [func(pixel, *args) for pixel in reshaped]

    return np.asarray(pixels).reshape(shape[0], shape[1], shape[2])
