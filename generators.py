from random import random
from ppl.utils import repeat
from matplotlib import pyplot
from functools import partial
from math import sqrt, cos, sin, pi, log


def normal(mu=0, sigma=1):
    r = random()
    phi = random()
    z = cos(2 * pi * phi) * sqrt(-2 * log(r))
    # z2 = sin(2 * pi * phi) * sqrt(-2 * log(r))
    return z * sigma + mu

samples = repeat(normal, 1000000)
pyplot.hist(samples, bins=20)
pyplot.show()

