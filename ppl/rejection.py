from ppl.interpretator import *


def rejection_query(model):
    """
    Simple rejection query implementation
    :param model:
    :param predicat:
    :param answer:
    :return:
    """
    while True:
        samples, predicat, answer = model()
        if predicat(*samples):
            return answer