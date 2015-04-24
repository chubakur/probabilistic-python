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
            return numpy.random.uniform(0, 1) <= p
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


def sample(erp, *params):
    """
    Generate sample from ERP
    :param erp:
    :type erp: ERP
    :param params:
    :return:
    """
    return erp.sample(*params)

flip = partial(sample, FlipERP())
uniform = partial(sample, UniformERP())
gaussian = partial(sample, GaussianERP())
beta = partial(sample, BetaERP())
poisson = partial(sample, PoissonERP())


if __name__ == '__main__':
    samples = repeat(gaussian, 100000)
    plot.hist(samples, bins=30)
    plot.show()
