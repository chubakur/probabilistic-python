def interpreter(_model, mh=False):
    """
    Execute the model, and return a scope
    :param _model:
    :type _model: str
    :return:
    :rtype: dict
    """
    _commands = _model[0:-2]
    for _command in _commands:
        exec _command
    __l = locals()
    del __l['_command']
    del __l['_commands']
    del __l['_model']
    return __l


def is_good_samples(_model, _sample):
    """
    If a sample satisfied the model conditions returns True
    :param _model:
    :type _model: str
    :param _sample:
    :type _sample: dict
    :return:
    :rtype: bool
    """
    _condition = _model[-1]
    if eval(_condition, None, _sample):
        return True
    return False


def get_variable(_model, _sample):
    _var = _model[-2]
    return eval(_var, None, _sample)