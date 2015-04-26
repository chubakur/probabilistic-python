from ppl.erp import *
from ppl.rejection import rejection_query
from functools import partial
from ppl.utils import repeat
from matplotlib import pyplot


def model():
    baserate = 0.1
    a = flip(p=baserate)
    b = flip(p=baserate)
    c = flip(p=baserate)
    d = a + b + c
    return locals()


def model2():
    a = uniform()
    b = uniform()
    c = a + b
    return locals()


for key, value in model().items():
    if isinstance(value, FixedERP):
        print key, value.sample().value()
    elif isinstance(value, StochasticValue):
        print key, value.value()

# def tst(x):
#     return x['d'] >= 2
#
# samples = repeat(partial(rejection_query, model, tst, lambda x: x['a'].sample().value()), 1000)
# pyplot.hist(samples)
# pyplot.show()
