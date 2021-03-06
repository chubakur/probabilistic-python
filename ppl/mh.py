# coding: utf-8
import inspect
from trace import Trace, Chunk
from math import log
from numpy.random import uniform
import numpy
import numpy.random
import random


class MCMC_shared:
    mh_flag = False
    iteration = 0
    trace = Trace()
    drift = 0.1


def trace_update(erp, name, *params):
    """
    Calls when ERP attemps to make sample
    :param erp:
    :param params:
    :return:
    """
    code_name = name
    if not code_name:
        stack = inspect.stack()
        for index, stack_call in enumerate(stack):
            frame, fname, line, module, code, idx = stack_call
            if module == 'mh_query':
                break
        frame, fname, line, module, code, idx = stack[index - 1]
        code_name = "%s%s-%s%d+%d" % (erp.__class__.__name__, str(params), module, line, index - 1)
    previous = MCMC_shared.trace.get(code_name)
    if previous:
        if previous.erp_parameters == params:
            MCMC_shared.trace._likelihood += erp.log_likelihood(previous.x, *params)
            MCMC_shared.trace.update(code_name, MCMC_shared.iteration)
        else:
            previous.erp_parameters = params
            MCMC_shared.trace._likelihood += erp.log_likelihood(previous.x, *params)
            MCMC_shared.trace.store(code_name, previous.erp_parameters, MCMC_shared.iteration)
        return previous.x
    else:
        x = erp.sample(*params)
        MCMC_shared.trace._likelihood += erp.log_likelihood(x, *params)
        MCMC_shared.trace.store(code_name, Chunk(erp, x, params), MCMC_shared.iteration)
        return x


def mh_query(model, pred, answer, samples_count, lag=1):
    """
    Metropolis-Hastings algorithm for sampling
    :param model: model to execute
    :param samples_count: how much samples we want
    :type samples_count: int
    :return: samples
    :rtype: list
    """
    MCMC_shared.mh_flag = True
    MCMC_shared.iteration = 0
    samples = []
    model()
    prev_name_idx = 0
    transitions = 0
    rejected = 0
    burn_in = 100
    miss = True
    while len(samples) < samples_count:
        MCMC_shared.iteration += 1
        variables = MCMC_shared.trace.names()
        # index = random.randint(0, len(variables) - 1)
        # selected_name = variables[index]
        selected_name = variables[prev_name_idx % len(MCMC_shared.trace.names())]
        prev_name_idx += 1
        current = MCMC_shared.trace.get(selected_name)
        erp, erp_params = current.erp, current.erp_parameters
        new_value = erp.proposal_kernel(current.x, *erp_params)
        # print erp_params
        fwdProb = erp.log_proposal_prob(current.x, new_value, *erp_params)
        rvsProb = erp.log_proposal_prob(new_value, current.x, *erp_params)
        # r и f для flip == 0
        # l = erp.log_likelihood(new_value, *erp_params)
        # new_trace = deepcopy(trace)
        new_trace = Trace(MCMC_shared.trace)
        new_trace.store(selected_name, Chunk(erp, new_value, erp_params), MCMC_shared.iteration)
        old_trace = MCMC_shared.trace
        MCMC_shared.trace = new_trace
        sample = model()
        MCMC_shared.trace = old_trace
        probability = log(uniform())
        # print sample
        # print new_trace._likelihood, old_trace._likelihood
        if probability < new_trace._likelihood - old_trace._likelihood + rvsProb - fwdProb and \
                (miss or pred(sample)):
            if miss and pred(sample):
                miss = False
            transitions += 1
            if not miss:
                if burn_in:
                    burn_in -= 1
                elif (transitions % lag) == 0:
                    # print len(samples), sample, new_trace._likelihood, rejected
                    samples.append(answer(sample))
            rejected = 0
            MCMC_shared.trace = new_trace
            MCMC_shared.trace.clean(MCMC_shared.iteration)
        else:
            rejected += 1

    return samples


def mh_query2(model, pred, answer, samples_count, lag=1):
    """
    Metropolis-Hastings algorithm for sampling
    :param model: model to execute
    :param samples_count: how much samples we want
    :type samples_count: int
    :return: samples
    :rtype: list
    """
    MCMC_shared.mh_flag = True
    MCMC_shared.iteration = 0
    samples = []
    miss = True
    model()
    transitions = 0
    rejection = 0
    while len(samples) < samples_count:
        MCMC_shared.iteration += 1
        variables = MCMC_shared.trace.get_vector()
        vector_vals_drift = variables.values()
        vector = [val[0] for val in vector_vals_drift]
        drifts = [val[1] for val in vector_vals_drift]
        shifted_vector = numpy.random.multivariate_normal(vector, numpy.diag(drifts))
        new_trace = Trace(MCMC_shared.trace)
        new_trace.set_vector(dict(zip(variables.keys(), shifted_vector.tolist())), MCMC_shared.iteration)
        old_trace = MCMC_shared.trace
        MCMC_shared.trace = new_trace
        sample = model()
        while not miss and new_trace._likelihood == -float("inf"):
            new_trace.clean(MCMC_shared.iteration)
            new_trace._likelihood = 0
            for name, (chunk, iteration) in new_trace.mem.items():
                if chunk.erp.log_likelihood(chunk.x, *chunk.erp_parameters) == -float("inf"):
                    new_chunk = Chunk(chunk.erp,
                                      numpy.random.normal(old_trace.get(name).x, chunk.drift / 2),
                                      chunk.erp_parameters,
                                      drift=chunk.drift)
                    new_trace.store(name, new_chunk, iteration)
            sample = model()
        MCMC_shared.trace = old_trace
        probability = log(uniform())
        # r = erp.log_proposal_prob()
        if probability < new_trace._likelihood - old_trace._likelihood and (miss or pred(sample)):
            if miss and pred(sample):
                miss = False
                MCMC_shared.drift = 0.05
            transitions += 1
            if (transitions % lag) == 0:
                if not miss:
                    # print sample, rejection
                    samples.append(answer(sample))
            rejection = 0
            MCMC_shared.trace = new_trace
            MCMC_shared.trace.clean(MCMC_shared.iteration)
        else:
            rejection += 1

    return samples