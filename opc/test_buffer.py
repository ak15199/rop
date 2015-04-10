from matrix import OPCBuffer
from colors import BLACK, RED
import numpy as np

M1X, M1Y = 3, 3
M2X, M2Y = 9, 9

m1 = OPCBuffer(M1X, M1Y)
m2 = OPCBuffer(M2X, M2Y)

def pixel_case(fromx, fromy, tox, toy, count):
    global m1, m2

    m1.buf[:][:] = BLACK
    m2.buf[:][:] = BLACK

    m2.buf[fromx:tox, fromy:toy] = RED
    m1.panCopy(m2, fromx, fromy)

    assert np.array_equal(m1.buf[0, 0], RED) and np.count_nonzero(m1.buf) == count

def area_case(fromx, fromy):

    m1.buf[:][:] = BLACK
    m2.buf[:][:] = BLACK

    m1.panCopy(m2, fromx, fromy)

    # these we expect to catch by exception
    return True

def test_copy_pixel_origin():
    pixel_case(0, 0, 1, 1, 1)

def test_copy_pixel_inset():
    pixel_case(4, 4, 5, 5, 1)

def test_copy_pixel_blockbegin():
    pixel_case(0, 0, 3, 3, 9)

def test_copy_pixel_blockwrap():
    pixel_case(6, 6, 8, 8, 4)

def test_copy_block_l():
    area_case(8, 0)

def test_copy_block_b():
    area_case(0, 8)

def test_copy_block_lb():
    area_case(8, 8)
