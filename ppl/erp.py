import numpy.random
from utils import repeat
from matplotlib import pyplot as plot
from functools import partial
from math import sqrt, exp, pi, log
import mh


class ERP:
    def __init__(self):
        self._generator = None

    def sample(self, *parameters):
        """
        Get sample by erp
        :param parameters: parameters of erp
        :return: sample
        :rtype: float
        """
        if self._generator:
            result = self._generator(*parameters)
            # trace.store(trace.get_name(), Chunk(self, result, parameters))
            return result
        raise Exception("Generator for %s does not set" % self.__class__.__name__)

    def likelihood(self, x, *parameters):
        """
        Get probability function of ERP on defined point
        :param x: point
        :type x: float
        :param parameters: parameters of erp
        :return: probability
        :rtype: float
        """
        raise Exception("Likelihood function for %s does not set" % self.__class__.__name__)

    def proposal_kernel(self, x, *parameters):
        """
        Propose next sample
        :param x: current point
        :type x: float
        :param parameters: parameters of erp
        :return: sample
        :rtype: float
        """
        return self.sample(*parameters)

    def log_proposal_prob(self, _from, _to, *parameters):
        return self.log_likelihood(_to, *parameters)

    def log_likelihood(self, x, *parameters):
        return log(self.likelihood(x, *parameters))


class FlipERP(ERP):
    def __init__(self):
        def _generator(p=0.5):
            return 1 if numpy.random.uniform(0, 1) <= p else 0

        self._generator = _generator

    def proposal_kernel(self, x, *parameters):
        return 0 if x else 1
        # return self.sample(*parameters)

    def log_proposal_prob(self, x, *parameters):
        return 0

    def likelihood(self, x, *parameters):
        probability = parameters[0]
        return probability if x else (1 - probability)


class UniformERP(ERP):
    def __init__(self):
        self._generator = numpy.random.uniform
        self._default_parameters = [0, 1]

    def log_likelihood(self, x, *parameters):
        if len(parameters) == 2:
            a, b = parameters
        elif len(parameters) == 1:
            a, b = parameters[0], self._default_parameters[1]
        else:
            a, b = self._default_parameters
        if a <= x <= b:
            return -log(b - a)
        return -float("inf")

    def proposal_kernel(self, x, *parameters):
        return numpy.random.normal(x, mh.drift)


class GaussianERP(ERP):
    def __init__(self):
        self._generator = numpy.random.normal
        self._default_parameters = [0, 1]

    def likelihood(self, x, *parameters):
        mu, sigma = parameters if parameters else self._default_parameters
        variance = sigma ** 2
        return exp(-(x - mu) ** 2 / (2 * variance)) / sqrt(2 * pi * variance)

    def proposal_kernel(self, x, *parameters):
        return self.sample(*[x, parameters[1] if len(parameters) == 2 else self._default_parameters[1]])

    def log_proposal_prob(self, _from, _to, *parameters):
        mu, sigma = parameters if parameters else self._default_parameters
        return self.log_likelihood(_to, *([_from] + list(parameters[1:])))

    def log_likelihood(self, x, *parameters):
        mu, sigma = parameters if parameters else self._default_parameters
        return -0.5 * (1.8378770664093453 + 2 * log(sigma) + (x - mu) ** 2 / (sigma ** 2))


class BetaERP(ERP):
    def __init__(self):
        self._generator = numpy.random.beta


class PoissonERP(ERP):
    def __init__(self):
        self._generator = numpy.random.poisson


class StochasticValue:
    def __init__(self, value):
        assert isinstance(value, (int, float))
        self._value = value

    def value(self):
        return self._value

    def __eq__(self, other):
        if isinstance(other, (int, float)):
            return self.value() == other
        elif isinstance(other, StochasticValue):
            return self.value() == other.value()

    def __gt__(self, other):
        if isinstance(other, (int, float)):
            return self.value() > other
        elif isinstance(other, StochasticValue):
            return self.value() > other.value()

    def __ge__(self, other):
        return self > other or self == other

    def __lt__(self, other):
        return not (self > other) and self != other

    def __le__(self, other):
        return self < other or self == other

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return StochasticValue(self.value() + other)
        elif isinstance(other, StochasticValue):
            return StochasticValue(self.value() + other.value())
        elif isinstance(other, FixedERP):
            return StochasticValue(self._value + other.sample()._value)


class FixedERP():
    def __init__(self, erp, params):
        """
        :param erp:
        :type erp: ERP
        """
        self.erp = erp
        self.params = params
        self.value = None

    def sample(self):
        if not self.value:
            self.value = StochasticValue(self.erp.sample(*self.params))
        return self.value

    def __float__(self):
        return self.sample()

    def __int__(self):
        return self.sample()

    def __add__(self, other):
        if isinstance(other, FixedERP):
            return self.sample() + other.sample()
        elif isinstance(other, int) or isinstance(other, float):
            return self.sample() + other


def sample(erp, name=None, *params):
    """
    Generate sample from ERP
    :param erp:
    :type erp: ERP
    :param params:
    :return:
    """
    if mh.mh_flag:
        return mh.trace_update(erp, name, *params)
    return erp.sample(*params)


# def flip(p=0.5):
# return FixedERP(FlipERP(), [p])
#
#
# def uniform(low=0., high=1.):
#     return FixedERP(UniformERP(), [low, high])

# flip = partial(sample, FlipERP())
uniform = partial(sample, UniformERP())
gaussian = partial(sample, GaussianERP())

if __name__ == '__main__':
    samples = repeat(gaussian, 100000)
    plot.hist(samples, bins=30)
    plot.show()
