from ppl.interpretator import *

a = 0
def rejection_query(model, predicat, answer):
    global a
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
            a += 1
            print "\r%d" % a,
            return answer(samples)


def rejection_query_(model):
    while True:
        samples = interpreter(model)
        if is_good_samples(model, samples):
            return get_variable(model, samples)