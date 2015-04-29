# coding: utf-8
from ppl.erp import *
from ppl.utils import repeat
from ppl.rejection import *
from matplotlib import pyplot as plot
from functools import partial
from ppl.mh import mh_query, mh_query2
from time import time
import ppl.mh


def model():
    threshold = 0.1
    a = flip(threshold)
    b = flip(threshold)
    c = flip(threshold)
    d = a + b + c
    return d


def model2():
    threshold = 0.1
    a = 1 if uniform() < threshold else 0
    b = 1 if uniform() < threshold else 0
    c = 1 if uniform() < threshold else 0
    d = a + b + c
    return d


def model3():
    if uniform() < 0.5:
        a = gaussian(10, 1)
    else:
        a = uniform(0, 10)
    b = gaussian(20, 1)
    return a * b + a


def model4():
    b = uniform(0, 10)
    return b


if __name__ == '__main__':
    _model = model3
    begin = time()
    samples_rejection_min = repeat(partial(rejection_query, _model, lambda x: True, lambda x: x), 10000)
    delta = time() - begin
    print 'Rejection-query-min:', delta
    begin = time()
    samples_rejection = repeat(partial(rejection_query, _model, lambda x: True, lambda x: x), 1000000)
    delta = time() - begin
    print 'Rejection-query:', delta
    begin = time()
    samples_mh = mh_query(_model, lambda x: True, lambda x: x, 10000, 10)
    delta = time() - begin
    print 'MH-query:', delta
    # begin = time()
    # samples_mh2 = mh_query2(_model, lambda x: True, lambda x: x, 10000, 1)
    # delta = time() - begin
    # print 'MH-query2:', delta
    bins = 50
    plot.figure(1)
    plot.title("RQmin")
    plot.hist(samples_rejection_min, bins=bins)
    plot.figure(2)
    plot.title("RQ")
    plot.hist(samples_rejection, bins=bins)
    plot.figure(3)
    plot.title("Gibbs")
    plot.hist(samples_mh, bins=bins)
    # plot.figure(4)
    # plot.title("MHQ")
    # plot.hist(samples_mh2, bins=bins)
    plot.show()
