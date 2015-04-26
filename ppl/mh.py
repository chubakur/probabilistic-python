import inspect
from trace import trace, Chunk, trace_update
from math import log
from numpy.random import uniform

mh_flag = False


def sampler(erp, *params):
    global trace
    stack = inspect.stack()
    frame, fname, line, module, code, idx = stack[2]
    code_name = "%s%d" % (module, line)
    previous = trace.get(code_name)
    if previous:
        erp, erp_params = previous.erp, previous.erp_parameters
        new_value = erp.proposal_kernel(previous.x, *erp_params)
        f = erp.log_proposal_prob(previous.x, *erp_params)
        r = erp.log_proposal_prob(new_value, *erp_params)
        l = erp.log_likelihood(new_value, *erp_params)
        new_trace = trace_update(trace)
        new_trace.store(code_name, Chunk(erp, new_value, erp_params))
        if log(uniform()) < new_trace.likelihood() - trace.likelihood() + r - f:
            trace = new_trace
            return new_value
        else:
            return previous.x
    else:
        random_value = erp.sample(*params)
        trace.store(code_name, Chunk(erp, random_value, params))
        return random_value


def mh_query(model, pred, val, samples_count):
    """
    Metropolis-Hastings algorithm for sampling
    :param model: model to execute
    :param samples_count: how much samples we want
    :type samples_count: int
    :return: samples
    :rtype: list
    """
    global mh_flag
    mh_flag = True
    samples = []
    while len(samples) < samples_count:
        sample = model()
        if pred(sample):
            samples.append(val(sample))
    mh_flag = False
    return samples