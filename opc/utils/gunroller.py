import numpy as np
from operator import mul

class GunRoller(object):

    def __init__(self, subject):
        self.shape = np.asarray(subject.shape)
        self.subject = subject

    def unroll(self):
        count = reduce(mul, self.shape, 1)
        reshaped = self.subject.reshape((count/3 ,3))
        rotated = np.rot90(reshaped)

        return rotated

    def reroll(self, subject):
        unrotated = np.rot90(subject, 3)
        unshaped = unrotated.reshape(self.shape)

        return unshaped
