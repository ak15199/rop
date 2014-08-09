import numpy as np

def process(buf, func, *args):
    shape = buf.shape
    reshaped = buf.reshape(shape[0]*shape[1], shape[2])

    pixels = [func(pixel, *args) for pixel in reshaped]

    return np.asarray(pixels).reshape(shape[0], shape[1], shape[2])
