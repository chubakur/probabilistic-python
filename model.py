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
    count = 100
    begin = time()
    samples_rejection = repeat(partial(rejection_query, model, lambda x: x[3] >= 2, lambda x: x[0]), count)
    delta = time() - begin
    print 'Rejection-query:', delta
    begin = time()
    samples_mh = mh_query(model, lambda x: x[3] >= 2, lambda x: x[0], count)
    delta = time() - begin
    print 'MH-query:', delta
    plot.figure(1)
    plot.hist(samples_rejection)
    plot.figure(2)
    plot.hist(samples_mh)
    plot.show()
