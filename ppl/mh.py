import inspect
from trace import Trace, Chunk
from math import log
from numpy.random import uniform
from copy import deepcopy
import random

mh_flag = False
trace = Trace()


def trace_update(erp, *params):
    """
    Calls when ERP attemps to make sample
    :param erp:
    :param params:
    :return:
    """
    global trace
    stack = inspect.stack()
    frame, fname, line, module, code, idx = stack[2]
    code_name = "%s%d" % (module, line)
    previous = trace.get(code_name)
    if previous:
        if previous.erp_parameters == params:
            pass
        else:
            previous.erp_parameters = params
            trace.store(code_name, previous.erp_parameters)
        return previous.x
    else:
        x = erp.sample(*params)
        trace.store(code_name, Chunk(erp, x, params))
        return x


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
    global mh_flag, trace
    mh_flag = True
    samples = []
    [model() for i in range(0, 10)]
    while len(samples) < samples_count:
        variables = trace.names()
        index = random.randint(0, len(variables) - 1)
        selected_name = variables[index]
        current = trace.get(selected_name)
        erp, erp_params = current.erp, current.erp_parameters
        new_value = erp.proposal_kernel(current.x, *erp_params)
        f = erp.log_proposal_prob(new_value, *erp_params)
        r = erp.log_proposal_prob(current.x, *erp_params)
        # l = erp.log_likelihood(new_value, *erp_params)
        n_trace = deepcopy(trace)
        n_trace.store(selected_name, Chunk(erp, new_value, erp_params))
        old_trace = trace
        trace = n_trace
        sample = model()
        trace = old_trace
        new_likelihood = n_trace.likelihood()
        old_likelihood = trace.likelihood()
        probability = log(uniform())
        if probability < new_likelihood - old_likelihood + r - f:
            if pred(sample):
                # print sample
                samples.append(val(sample))
        trace = n_trace

    return samples