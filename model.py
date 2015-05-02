# coding: utf-8
from ppl.erp import *
from ppl.utils import repeat
from ppl.rejection import *
# from matplotlib import pyplot as plot
from functools import partial
from ppl.mh import mh_query, mh_query2
from time import time
import ppl.mh


def model():
    def good(a, b, c, d):
        return d >= 2

    threshold = 0.01
    a = flip(threshold, name='m1a')
    b = flip(threshold, name='m1b')
    c = flip(threshold, name='m1c')
    d = a + b + c
    return [a, b, c, d], good, a


def model1p():
    def good(a, b, c, d, e):
        return e >= 3

    threshold = 0.01
    a = flip(threshold, name='m1pa')
    b = flip(threshold, name='m1pb')
    c = flip(threshold, name='m1pc')
    d = flip(threshold, name='m1pd')
    e = a + b + c + d
    return [a, b, c, d, e], good, a


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
    _model = model1p
    begin = time()
    samples_rejection_min = repeat(partial(rejection_query, _model), 1000)
    # samples_rejection_min = [1, 2]
    delta = time() - begin
    print 'Rejection-query-min:', delta, len(filter(lambda x: x, samples_rejection_min)) / float(
        len(samples_rejection_min))
    begin = time()
    samples_gibbs = mh_query(_model, 1000, 10)
    delta = time() - begin
    print 'Gibbs-query:', delta, len(filter(lambda x: x, samples_gibbs)) / float(len(samples_gibbs))
    begin = time()
    samples_mh = mh_query2(_model, 1000, 1)
    delta = time() - begin
    print 'MH-query:', delta, len(filter(lambda x: x, samples_mh)) / float(len(samples_mh))
    # bins = 2
    # plot.figure(1)
    # plot.title("Rejection")
    # plot.hist(samples_rejection_min, bins=bins)
    # plot.figure(3)
    # plot.title("Gibbs")
    # plot.hist(samples_gibbs, bins=bins)
    # plot.figure(5)
    # plot.title("Metropolis-Hastings")
    # plot.hist(samples_mh, bins=bins)
    # plot.show()
