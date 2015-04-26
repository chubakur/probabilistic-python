from ppl.erp import *
from ppl.utils import repeat
from ppl.rejection import *
from matplotlib import pyplot as plot
from functools import partial
from ppl.mh import mh_query
from time import time


def model():
    threshold = 0.1
    a = flip(threshold)
    b = flip(threshold)
    c = flip(threshold)
    d = a + b + c
    return [a, b, c, d]

if __name__ == '__main__':
    begin = time()
    # samples = repeat(partial(rejection_query, model, lambda x: x[3] >= 2, lambda x: x[0]), 100)
    samples = mh_query(model, lambda x: x[3] >= 2, lambda x: x[0], 100)
    delta = time() - begin
    print delta
    plot.hist(samples)
    plot.show()
