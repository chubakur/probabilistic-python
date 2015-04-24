from numpy import random
import numpy
from functools import partial
from matplotlib import pyplot
from copy import deepcopy, copy
from math import sqrt


def flip(p):
    return random.uniform() < p


def rejection_query(variables, condition, return_value):
    _scope = dict()
    [variable.set_scope(_scope) for variable in variables]
    [variable.set_vars(variables) for variable in variables]
    iteration = 0
    while True:
        iteration += 1
        for variable in variables:
            _scope[variable.name()] = variable.get()
        code = condition
        for name in _scope.keys():
            code = code.replace(name, "_scope['%s']" % name)
        if eval(code):
            print iteration
            return _scope[return_value]


def mh_query(variables, condition, return_value, samples_cnt, lag):
    _scope = dict()
    step = 0.05
    samples = []
    burning = 1000
    [variable.set_scope(_scope) for variable in variables]
    [variable.set_vars(variables) for variable in variables]
    while burning:
        burning -= 1
        for variable in variables:
            _scope[variable.name()] = variable.get()
    vv = variables[-1]
    cur_point = dict([(v.name(), v.last_value()) for v in variables if v.is_dirty()])
    l = 0
    while len(samples) < samples_cnt:
        new_point = dict()
        for key, value in cur_point.items():
            new_point[key] = random.normal(value, 0.1)
        p = float(vv.probability(new_point))/float(vv.probability(cur_point))
        if random.random() < p:
            cur_point = new_point
            _scope.update(new_point)
            _scope[vv.name()] = vv.get()
            print _scope
            code = condition
            for name in _scope.keys():
                code = code.replace(name, "_scope['%s']" % name)
            if eval(code):
                if l:
                    l -= 1
                    continue
                samples.append(_scope[return_value])
                l = 0
                print samples
    return samples


def repeat(num, func):
    result = []
    for i in range(0, num):
        result.append(func())
    return result


class Variable:
    def __init__(self, name, fnc, prob_func=None):
        self._name = name
        self._fnc = fnc
        self._scope = None
        self._vars = []
        self._lret = None
        self._prob_func = prob_func

    def probability(self, x):
        def _probability(name, x):
            for var in self._vars:
                if var.name() == name:
                    return var.probability(x)
            raise IndexError
        if callable(self._prob_func):
            return self._prob_func(x)
        template = self._fnc
        if not isinstance(template, str):
            print type(template)
        for key in self._scope.keys():
            if key in template:
                template = template.replace(key, "_probability('%s', %d)" % (key, x[key]))
        return eval(template)

    def set_vars(self, vars):
        self._vars = vars

    def is_dirty(self):
        return callable(self._fnc)

    def set_scope(self, _scope):
        self._scope = _scope

    def get(self):
        if callable(self._fnc):
            self._lret = self._fnc()
            return self._lret
        result = self._fnc
        for name in self._scope.keys():
            result = result.replace(name, "self._scope['%s']" % name)
        self._lret = eval(result)
        return self._lret

    def last_value(self):
        return self._lret

    def name(self):
        return self._name


class Variables:
    def __init__(self, variables):
        self.variables = variables

    def get(self, variable_name):
        for variable in self.variables:
            if variable.name() == variable_name:
                return variable.get()
        raise IndexError


def breast_cancer_model():
    breast_cancer = Variable('breast-cancer', partial(flip, 0.01), prob_func=p_flip(0.01))
    positive_mammogram = Variable('positive-mammogram', "flip(0.8 if breast-cancer else 0.096)")
    return [breast_cancer, positive_mammogram], "breast-cancer", "positive-mammogram"
    # return partial(rejection_query, [breast_cancer, positive_mammogram], "breast-cancer", "positive-mammogram")


def my_model():
    a = Variable("A", random.standard_normal, prob_func=p_gaussn())
    b = Variable("B", random.standard_normal, prob_func=p_gaussn())
    c = Variable("C", partial(random.normal, 2, 1), prob_func=p_gaussn(2, sqrt(1)))
    d = Variable("D", "A + B + C")
    # d = Variable("D", "A + B - C")
    return [a, b, c, d], "D > 3.5", "A"
    # return partial(rejection_query, [a, b, c, d],  "D > 3.5", "C")


def p_gaussn(mu=0, sigma=1):
    def f(x):
        _a = 1/(sigma * numpy.sqrt(2*numpy.pi))
        _b = - (x - mu)**2/(2*(sigma**2))
        return _a * numpy.exp(_b)
    return f


def p_uniform(a=0, b=1):
    def f(x):
        if a <= x <= b:
            return 1/(b - a)
        return 0
    return f


def p_flip(a):
    def f(x):
        if x <= a:
            return 1.0
        return 0.0
    return f


if __name__ == '__main__':
    # x = numpy.arange(-5, 5, 0.01)
    # standard = p_gaussn(sigma=numpy.sqrt(1))
    # y = map(standard, x)
    # pyplot.plot(x, y)
    # pyplot.show()
    # model = my_model()
    # answers = repeat(1000, model)
    # pyplot.hist(answers, bins=10)
    # pyplot.show
    vars, cond, ret = my_model()
    pyplot.hist(repeat(100, partial(rejection_query, vars, cond, ret)))
    pyplot.show()
    pyplot.hist(mh_query(vars, cond, ret, 100, 100))
    pyplot.show()