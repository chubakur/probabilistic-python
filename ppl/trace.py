import inspect
import warnings
from copy import deepcopy


class Chunk:
    def __init__(self, erp, x, erp_parameters):
        """
        :param erp:
        :type erp: ERP
        :param x:
        :param erp_parameters:
        :return:
        """
        self.erp = erp
        self.x = x
        self.erp_parameters = erp_parameters


class Trace:
    def __init__(self):
        self.mem = dict()

    def get_name(self):
        """
        Get name for caller
        :return: name
        :rtype: str
        """
        stack = inspect.stack()
        frame, filename, line, module, code, index = stack[2]
        warnings.warn("Simple trace name generator can wrong on complex models")
        return "%s-%s" % (module, line)

    def get(self, name):
        """
        Search previous result
        :param name: name
        :type name: str
        :return: result of previous evaluation this string
        :rtype: Chunk or None
        """
        if name in self.mem:
            return self.mem[name]
        return None

    def names(self):
        """
        Return all stored names
        :return:
        :rtype: list
        """
        return self.mem.keys()

    def store(self, name, chunk):
        """
        Store result of evaluation
        :param name: name
        :type name: str
        :param chunk: result
        :type chunk: Chunk
        """
        self.mem[name] = chunk

    def likelihood(self):
        """
        Return sum of likelihood of each stochastic variable
        :return: likelihood
        :rtype: float
        """
        _ll = 0
        for name, chunk in self.mem.items():
            _ll += chunk.erp.log_likelihood(chunk.x, *chunk.erp_parameters)
        return _ll


def trace_update(_trace):
    """
    Function which update trace
    :param _trace: trace object
    :type _trace: Trace
    :return: Updated trace object
    :rtype: Trace
    """
    _new_trace = deepcopy(_trace)
    # TODO: WTF???
    return _new_trace