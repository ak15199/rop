from random import random

from opc.utils.prof import timefunc

# implementation of a linear feedback shift register generator that gives us
# n-bits of pseudo-random values, completing the entire sequence before
# repeating.

# polynomials required to calculate a n-bit lsfr. Higher bits are
# available, just not included here yet.
poly = {
    2:  (2, 1),
    3:  (3, 2),
    4:  (4, 3),
    5:  (5, 3),
    6:  (6, 5),
    7:  (7, 6),
    8:  (8, 6, 5, 4),
    9:  (9, 5),
    10: (10, 7),
    11: (11, 9),
    12: (12, 11, 14),
    13: (13, 12, 11, 8),
    14: (14, 13, 12, 2),
    15: (15, 14),
    16: (16, 14, 13, 11),
    }


def bit(value, bit):
    return (value >> bit) & 1


@timefunc
def lfsr(seed=None, bits=8, base=0):
    """
    simulate a LFSR for a given number of bits. Seed=0 is special
    in that it specifies that a random value should be chosen as the
    seed
    """
    if seed is None:
        seed = bits
    elif seed == 0:
        seed = int(random()*(2**bits-1))

    try:
        toggles = poly[bits]
    except:
        raise Exception("%d bit LFSRs aren't supported" % bits)

    lfsr = seed
    starting = True
    while lfsr != seed or starting:
        yield base+lfsr
        starting = False

        tap = 0
        for toggle in toggles:
            position = bits-toggle
            tap ^= bit(lfsr, position)

        lfsr = (lfsr >> 1) | (tap << bits-1)

    yield base


class LfsrBucket(object):

    def __init__(self, slots, base=0):
        self.content = []
        self.ptr = 0

        # figure out our base power. If this is first time
        # in, and there is enough elbow room, then start with
        # a slightly smaller chunk (to improve distribution)
        power = self._invPow2(slots)
        if base == 0 and power > 2:
            power -= 1

        while slots >= 2**power:
            self._addLfsr(power, base)
            slots -= 2**power
            base += 2**power

        # if there's anything left over, deal with it as a
        # sub-bucket
        if slots > 0:
            self._addBucket(slots, base)

    def _invPow2(self, value):
        """
        This is a brute force approach to get the closest power of two
        that is greater than the value presented. But it will give
        adequate performance, given our application.
        """
        power = 0
        while 2**power <= value:
            power += 1

        return power-1

    def _addLfsr(self, bits, base):
        self.content.append(lfsr(seed=0, bits=bits, base=base))

    def _addBucket(self, slots, base):
        self.content.append(LfsrBucket(slots, base))

    def buckets(self):
        return len(self.content)

    @timefunc
    def get(self, level=0):
        """
        Get the next value from the bucket. A candidate can either
        be a LFSR, or it can be a sub-bucket. We'll need to check
        for all and handle exceptions appropriately.
        """
        candidate = self.content[self.ptr]
        self.ptr = (self.ptr+1) % len(self.content)

        try:
            return candidate.get(level+1)
        except AttributeError:
            try:
                return candidate.next()
            except StopIteration:
                return None


@timefunc
def compoundLfsr(slots):
    """
    Combine a number of LFSRs to support an arbitary range of
    once-visit values, most of the heavy lifting is done in a
    class.

    figure out largest power of two that is smaller than places
    add as many of these to the pool that fit, this is a bucket.
    take the remainder and repeat until there is nothing left.

    while generating visit each bucket in round-robin sequence,
    until all of the buckets report empty.
    """
    pool = LfsrBucket(slots)
    while True:
        failures = 0
        while True:
            value = pool.get()
            if value is not None:
                yield value
                break

            failures += 1
            if failures == pool.buckets():
                # nome of the buckets have anything left, the
                # supply of values is exhausted
                return
