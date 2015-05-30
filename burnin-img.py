from matplotlib import pyplot
from numpy.random import normal
import numpy

# def step(x):
#     return 0.98 * x + normal(0, 0.1)
#
# SIZE = 1000
#
# def generate_points(x):
#     result = []
#     for i in range(0, SIZE):
#         x = step(x)
#         result.append(x)
#     return result
#
# pyplot.figure(0)
# pyplot.plot(range(0, SIZE), generate_points(10), 'k.', label='x=10')
# pyplot.figure(1)
# pyplot.plot(range(0, SIZE), generate_points(0), 'k.', label='x=0')
# pyplot.show()

y = []
x = 2
for i in range(0, 1000):
    x = 0.96 * x + normal(1, 0.1)
    y.append(x)

yd = numpy.array(y)
print yd.mean()
pyplot.plot(range(0, len(y)), y, 'k.')
pyplot.show()
