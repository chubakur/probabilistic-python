from ppl.erp import *
from ppl.utils import repeat
from ppl.rejection import *
from matplotlib import pyplot as plot
from functools import partial
from ppl.mh import mh_query

model = """
baserate = 0.2
a = 1 if flip(baserate) else 0
b = 1 if flip(baserate) else 0
c = 1 if flip(baserate) else 0
d = a + b + c
a
d >= 2
"""


if __name__ == '__main__':
    # plot.hist(repeat(partial(rejection_query_, model.strip().split('\n')), 100))
    plot.hist(mh_query(model.strip().split('\n'), 100))
    plot.show()
