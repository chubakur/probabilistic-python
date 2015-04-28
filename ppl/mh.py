# coding: utf-8
import inspect
from trace import Trace, Chunk
from math import log
from numpy.random import uniform
from copy import deepcopy
import numpy
import numpy.random

mh_flag = False
iteration = 0
trace = Trace()
drift = 0.1


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
            trace.update(code_name, iteration)
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


def mh_query(model, pred, val, samples_count, lag=1):
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
    iteration = 0
    samples = []
    for i in range(0, 100):
        trace._likelihood = 0
        trace.clean(iteration)
        iteration += 1
        model()
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
        # print erp_params
        fwdProb = erp.log_proposal_prob(current.x, new_value, *erp_params)
        rvsProb = erp.log_proposal_prob(new_value, current.x, *erp_params)
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
        # print new_trace._likelihood, old_trace._likelihood
        if probability < new_trace._likelihood - old_trace._likelihood + rvsProb - fwdProb:
            transitions += 1
            if (transitions % lag) == 0:
                # print len(samples), sample, new_trace._likelihood
                samples.append(val(sample))
            trace = new_trace
            trace.clean(iteration)

    return samples


def mh_query2(model, pred, val, samples_count, lag=1):
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
    iteration = 0
    samples = []
    for i in range(0, 100):
        trace._likelihood = 0
        trace.clean(iteration)
        iteration += 1
        model()
    transitions = 0
    while len(samples) < samples_count:
        iteration += 1
        new_trace = deepcopy(trace)
        variables = trace.get_vector()
        vector = variables.values()
        shifted_vector = numpy.random.multivariate_normal(vector, numpy.diag([0.1] * len(vector)))
        new_trace.set_vector(dict(zip(variables.keys(), shifted_vector.tolist())), iteration)
        old_trace = trace
        trace = new_trace
        new_trace._likelihood = 0
        sample = model()
        trace = old_trace
        probability = log(uniform())
        # print new_trace._likelihood, old_trace._likelihood
        if probability < new_trace._likelihood - old_trace._likelihood:
            transitions += 1
            if (transitions % lag) == 0:
                print len(samples)
                samples.append(val(sample))
            trace = new_trace
            trace.clean(iteration)

    return samples