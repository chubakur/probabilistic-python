from trace import Trace
from interpretator import *


def trace_update():
    pass


def mh_query(model, count):
    """
    Metropolis-Hastings algorithm for sampling
    :param model: model to execute
    :param count: how much samples we want
    :type count: int
    :return: samples
    :rtype: list
    """
    # burning model
    # [model() for _ in range(0, 100)]
    trace = Trace()
    samples = []
    execute_queue = model[0:-2]
    while len(samples) < count:
        for idx, execute_agent in enumerate(execute_queue):
            if 'flip' in execute_agent:
                if trace.get(str(idx)):
                    pass
                else:
                    pass

        break
    return samples