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

if __name__ == '__main__':
    # условия очистки. считать кол-во итераций, и обновлять у трейса номер итерации. у кого не совпал - в топку.
    # ppl.mh.mh_flag = True
    # for i in xrange(0, 100):
    #     print model()
    # exit()
    count = 100
    begin = time()
    samples_rejection = repeat(partial(rejection_query, model2, lambda x: True, lambda x: x), 100000)
    delta = time() - begin
    print 'Rejection-query:', delta
    begin = time()
    samples_mh = mh_query(model2, lambda x: True, lambda x: x, 10000)
    delta = time() - begin
    print 'MH-query:', delta
    begin = time()
    samples_mh2 = mh_query2(model2, lambda x: True, lambda x: x, 10000)
    delta = time() - begin
    print 'MH-query2:', delta
    plot.figure(1)
    plot.hist(samples_rejection)
    plot.figure(2)
    plot.hist(samples_mh)
    plot.figure(3)
    plot.hist(samples_mh2)
    plot.show()
