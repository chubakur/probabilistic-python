def repeat(func, times):
    """
    Repeat function N-times and return N-results
    :param func: function to exec
    :param times: N
    :type times: int
    :return: list
    :rtype: list
    """
    return [func() for i in range(0, times)]