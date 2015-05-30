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


def model1p():
    threshold = 0.01
    a = flip(threshold, name='m1pa')
    b = flip(threshold, name='m1pb')
    c = flip(threshold, name='m1pc')
    d = flip(threshold, name='m1pd')
    e = a + b + c + d
    return [a, b, c, d, e]


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
    return 0 if flip(p) else (geometric(p) + 1)


# def pred(sample):
#     return True
#
#
# def answer(sample):
#     return sample


def pred(sample):
    a, b, c, d = sample
    return d >= 2


def answer(sample):
    a, b, c, d = sample
    return a


if __name__ == '__main__':
    _model = model
    # begin = time()
    # samples_rejection_min = repeat(partial(rejection_query, _model, pred, answer), 10000)
    # samples_rejection_min = [1, 2]
    # delta = time() - begin
    # print 'Rejection-query-min:', delta, len(filter(lambda x: x, samples_rejection_min)) / float(
    #     len(samples_rejection_min))
    # doles = []
    begin = time()
    samples_gibbs = mh_query(_model, pred, answer, 1000, 50)
    print time() - begin
    # for i in range(0, 100):
    #     begin = time()
    #     samples_gibbs = mh_query(_model, pred, answer, 1000, 50)
    #     delta = time() - begin
    #     d = len(filter(lambda x: x, samples_gibbs)) / float(len(samples_gibbs))
    #     print 'Gibbs-query:', delta, d
    #     doles.append(d)
    # print min(doles), max(doles), sum(doles) / len(doles)
    # begin = time()
    # samples_mh = mh_query2(_model, pred, answer, 1000, 1)
    # delta = time() - begin
    # print 'MH-query:', delta, len(filter(lambda x: x, samples_mh)) / float(len(samples_mh))
    bins = 2
    # plot.figure(1)
    # plot.title("Rejection")
    # plot.hist(samples_rejection_min)
    plot.figure(3)
    plot.title("Gibbs")
    plot.hist(samples_gibbs, bins=bins)
    # plot.figure(5)
    # plot.title("Metropolis-Hastings")
    # plot.hist(samples_mh, bins=bins)
    plot.show()
