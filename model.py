from ppl.erp import *
from ppl.utils import repeat
from ppl.rejection import *
from matplotlib import pyplot as plot
from functools import partial
from ppl.mh import mh_query


if __name__ == '__main__':
    # plot.hist(repeat(partial(rejection_query_, model.strip().split('\n')), 100))
    plot.hist(mh_query(model.strip().split('\n'), 100))
    plot.show()
