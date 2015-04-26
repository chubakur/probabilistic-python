from ppl.interpretator import *


def rejection_query(model, predicat, answer):
    """
    Simple rejection query implementation
    :param model:
    :param predicat:
    :param answer:
    :return:
    """
    while True:
        samples = model()
        if predicat(samples):
            return answer(samples)


def rejection_query_(model):
    while True:
        samples = interpreter(model)
        if is_good_samples(model, samples):
            return get_variable(model, samples)