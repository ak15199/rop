#
# implementation of a linear feedback shift register. this gives us
# 255 pseudo-random values, completing the entire sequence before
# repeating
#

def bit(value, bit):
    return (value >> bit) & 1

def lfsr(seed=0x8, bits=8):
    lfsr = seed
    period = 0
 
    while period < 255:
        period += 1
        tap = bit(lfsr, 0) ^ bit(lfsr, 4) ^ bit(lfsr, 5) ^ bit(lfsr, 6)
        lfsr = (lfsr >> 1) | (tap << bits-1)
        yield lfsr
