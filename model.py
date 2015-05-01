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
    threshold = 0.01
    a = flip(threshold, name='m1a')
    b = flip(threshold, name='m1b')
    c = flip(threshold, name='m1c')
    d = a + b + c
    return [a, b, c, d]

def model1Plus():
    threshold = 0.01
    a = flip(threshold, name='m1pa')
    b = flip(threshold, name='m1pb')
    c = flip(threshold, name='m1pc')
    d = flip(threshold, name='m1pd')
    e = a + b + c + d
    return [a, b, c, d, e]


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
    a = 0.7 if flip(name="m4a") else 0.1
    b = flip(a, name="m4b")
    return b


def flip(a=0.5, **kwargs):
    return uniform(**kwargs) < a


def geometric(p):
    cont = flip(p)
    if cont:
        return 1 + geometric(p)
    return 0
    # return (geometric(p) + 1) if flip(p) else 0


if __name__ == '__main__':
    _model = model1Plus
    begin = time()
    samples_rejection_min = repeat(partial(rejection_query, _model, lambda x: x[4] >= 3, lambda x: x[0]), 1000)
    delta = time() - begin
    print 'Rejection-query-min:', delta
    # begin = time()
    # samples_rejection = repeat(partial(rejection_query, _model, lambda x: True, lambda x: x), 1000)
    # delta = time() - begin
    # print 'Rejection-query:', delta
    begin = time()
    # import cProfile
    # cProfile.run("mh_query(_model, lambda x: True, lambda x: x, 10000, 1)")
    samples_mh = mh_query(_model, lambda x: x[4] >= 3, lambda x: x[0], 1000, 10)
    # samples_mh = [1, 2]
    delta = time() - begin
    print 'MH-query:', delta
    # begin = time()
    # samples_mh2 = mh_query2(_model, lambda x: True, lambda x: x, 10000, 100)
    # delta = time() - begin
    # print 'MH-query2:', delta
    bins = 2
    plot.figure(1)
    plot.title("IDEAL")
    plot.hist(samples_rejection_min, bins=bins)
    # plot.figure(2)
    # plot.title("RQmin")
    # plot.hist(samples_rejection, bins=bins)
    plot.figure(3)
    plot.title("Gibbs")
    plot.hist(samples_mh, bins=bins)
    # plot.figure(4)
    # plot.title("MHQ")
    # plot.hist(samples_mh2, bins=bins)
    plot.show()
