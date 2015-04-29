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
    def __init__(self, trace=None):
        if not trace:
            self.mem = dict()
            self._likelihood = 0.
        else:
            self._likelihood = 0.
            self.mem = dict(trace.mem)

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
            return self.mem[name][0]
        return None

    def names(self):
        """
        Return all stored names
        :return:
        :rtype: list
        """
        return self.mem.keys()

    def get_vector(self):
        """

        :return:
        :rtype: dict
        """
        result = dict()
        for name, chunk in self.mem.items():
            result[name] = chunk[0].x
        return result

    def set_vector(self, vector, iteration):
        for name, value in vector.items():
            chunk, _ = self.mem[name]
            self.mem[name] = chunk, iteration
            chunk.x = value

    def store(self, name, chunk, iteration=0):
        """
        Store result of evaluation
        :param name: name
        :type name: str
        :param chunk: result
        :type chunk: Chunk
        """
        self.mem[name] = chunk, iteration

    def update(self, name, iteration):
        """
        Update last_access_iter number
        :param name:
        :param iteration:
        :return:
        """
        self.mem[name] = self.mem[name][0], iteration

    def clean(self, iteration):
        for k in self.mem.keys():
            if self.mem[k][1] < iteration:
                del self.mem[k]