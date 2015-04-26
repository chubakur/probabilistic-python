import numpy.random
from utils import repeat
from matplotlib import pyplot as plot
from functools import partial
from math import sqrt, exp, pi


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
        raise Exception("Proposal kernel function for %s does not set" % self.__class__.__name__)


class FlipERP(ERP):
    def __init__(self):
        def _generator(p=0.5):
            return 1 if numpy.random.uniform(0, 1) <= p else 0
        self._generator = _generator


class UniformERP(ERP):
    def __init__(self):
        self._generator = numpy.random.uniform
        self._default_parameters = [0, 1]

    def likelihood(self, x, *parameters):
        a, b = parameters if parameters else self._default_parameters
        if a <= x <= b:
            return 1/(b - a)
        return 0


class GaussianERP(ERP):
    def __init__(self):
        self._generator = numpy.random.normal
        self._default_parameters = [0, 1]

    def likelihood(self, x, *parameters):
        mu, sigma = parameters if parameters else self._default_parameters
        variance = sigma**2
        return exp(-(x-mu)**2/(2*variance))/sqrt(2*pi*variance)


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


def sample(erp, *params):
    """
    Generate sample from ERP
    :param erp:
    :type erp: ERP
    :param params:
    :return:
    """
    return erp.sample(*params)


# def flip(p=0.5):
#     return FixedERP(FlipERP(), [p])
#
#
# def uniform(low=0., high=1.):
#     return FixedERP(UniformERP(), [low, high])

flip = partial(sample, FlipERP())
uniform = partial(sample, UniformERP())


if __name__ == '__main__':
    samples = repeat(gaussian, 100000)
    plot.hist(samples, bins=30)
    plot.show()
