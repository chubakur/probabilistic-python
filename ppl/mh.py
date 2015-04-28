# coding: utf-8
import inspect
from trace import Trace, Chunk
from math import log
from numpy.random import uniform
from copy import deepcopy
import random

mh_flag = False
iteration = 0
trace = Trace()


def trace_update(erp, *params):
    """
    Calls when ERP attemps to make sample
    :param erp:
    :param params:
    :return:
    """
    global trace, iteration
    stack = inspect.stack()
    frame, fname, line, module, code, idx = stack[2]
    code_name = "%s%d" % (module, line)
    previous = trace.get(code_name)
    if previous:
        if previous.erp_parameters == params:
            trace._likelihood += erp.log_likelihood(previous.x, *params)
        else:
            previous.erp_parameters = params
            trace._likelihood += erp.log_likelihood(previous.x, *params)
            trace.store(code_name, previous.erp_parameters, iteration)
        return previous.x
    else:
        x = erp.sample(*params)
        trace._likelihood += erp.log_likelihood(x, *params)
        trace.store(code_name, Chunk(erp, x, params), iteration)
        return x


def mh_query(model, pred, val, samples_count):
    """
    Metropolis-Hastings algorithm for sampling
    :param model: model to execute
    :param samples_count: how much samples we want
    :type samples_count: int
    :return: samples
    :rtype: list
    """
    global mh_flag, trace, iteration
    mh_flag = True
    samples = []
    [model() for i in range(0, 100)]
    prev_name_idx = 0
    transitions = 0
    while len(samples) < samples_count:
        iteration += 1
        variables = trace.names()
        # index = random.randint(0, len(variables) - 1)
        selected_name = variables[prev_name_idx % len(trace.names())]
        prev_name_idx += 1
        current = trace.get(selected_name)
        erp, erp_params = current.erp, current.erp_parameters
        new_value = erp.proposal_kernel(current.x, *erp_params)
        f = erp.log_proposal_prob(new_value, *erp_params)
        r = erp.log_proposal_prob(current.x, *erp_params)
        # r и f для flip == 0
        # l = erp.log_likelihood(new_value, *erp_params)
        new_trace = deepcopy(trace)
        new_trace.store(selected_name, Chunk(erp, new_value, erp_params), iteration)
        old_trace = trace
        trace = new_trace
        new_trace._likelihood = 0
        sample = model()
        trace = old_trace
        probability = log(uniform())
        print new_trace._likelihood, old_trace._likelihood
        if probability < new_trace._likelihood - old_trace._likelihood + r - f:
            transitions += 1
            if (transitions % 1) == 0:
                print len(samples)
                samples.append(val(sample))
            trace = new_trace
            trace.clean(iteration)

    return samples