import numpy
from matplotlib import pyplot
from matplotlib import patches
from math import sqrt, pi, exp


def gaussian(x, mu=0, sigma=1):
    variance = sigma ** 2
    return exp(-(x - mu) ** 2 / (2 * variance)) / sqrt(2 * pi * variance)

if __name__ == '__main__':
    x = numpy.arange(-4, 4, 0.01)
    y = map(gaussian, x)
    pyplot.plot(x, y)
    pyplot.plot([1], [0], 'go')
    circle = patches.Circle([1, 0], 1)
    print circle
    pyplot.show()
