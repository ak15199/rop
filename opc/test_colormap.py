from colormap import Colormap
import numpy as np


def test_soften():
    c = Colormap(10)
    c.flat(0, 10, (0, 0, 0))
    c.flat(3, 6, (255, 128, 64))

    c.soften()

    assert np.array_equal(c.cmap, [
                          [0, 0, 0],
                          [0, 0, 0],
                          [63, 32, 16],
                          [191, 96, 48],
                          [255, 128, 64],
                          [191, 96, 48],
                          [63, 32, 16],
                          [0, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]
                          ]), "Array didn't soften properly"


def test_rotate():
    c = Colormap(130)
    c.flat(0, 130, (0, 0, 0))
    c.flat(0, 1, (1, 1, 1))

    v1 = sum(c.cmap[0])
    c.rotate(1)

    assert np.array_equal(c.cmap[0], [0, 0, 0]), \
        "Array 0th element didn't shift out (%s)" % str(c.cmap[0])
    assert np.array_equal(c.cmap[1], [1, 1, 1]), \
        "Array 1st element didn't shift in (%s)" % str(c.cmap[1])

    v2 = sum(c.cmap[0])
    c.rotate(-1)
    v3 = sum(c.cmap[0])

    # when we rotate out and rotate back, there should be net zero change to
    # the value of the first element. But the interim first element shoud be
    # different
    assert v1 == v3, "Array didn't rotate back (0)"
    assert v2 != v3, "Array didn't rotate back (1)"
