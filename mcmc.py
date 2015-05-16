import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.mlab as mlab
import scipy.stats as stats
import random

delta = 0.025
X, Y = np.meshgrid(np.arange(-4.5, 2.0, delta), np.arange(-3.5, 3.5, delta))

z1 = stats.multivariate_normal(mean=[0, 0], cov=[[1.0, 0], [0, 1.0]])
z2 = stats.multivariate_normal(mean=[-2, -2], cov=[[1.5, 0], [0, 0.5]])


def z(x):
    return 0.4 * z1.pdf(x) + 0.6 * z2.pdf(x)

Z1 = mlab.bivariate_normal(X, Y, sigmax=1.0, sigmay=1.0, mux=0.0, muy=0.0)
Z2 = mlab.bivariate_normal(X, Y, sigmax=1.5, sigmay=0.5, mux=-2, muy=-2)
Z = 0.4 * Z1 + 0.6 * Z2

Q = stats.multivariate_normal([0, 0], [[0.05, 0], [0, 0.05]])
r = [0, 0]
samples = [r]
# z1s = [z1.rvs() for i in range(0, 10000)]

for i in range(0, 1000):
    # random = Q.rvs()
    single_random = np.random.normal(0, 0.5)
    random = np.zeros((len(r), ))
    random[0] = single_random
    np.random.shuffle(random)
    rq = random + r
    a = z(rq) / z(r)
    if np.random.binomial(1, min(a, 1), 1)[0] == 1:
        # if z1.pdf(rq) > 0 and z2.pdf(rq) > 0:
        # print z1.pdf(rq), z2.pdf(rq)
        r = rq
        samples.append(r)

codes = np.ones(len(samples), int) * path.Path.LINETO
codes[0] = path.Path.MOVETO

p = path.Path(samples, codes)

# plt.contour(X, Y, Z)

fig, ax = plt.subplots()
ax.contour(X, Y, Z)
ax.add_patch(patches.PathPatch(p, facecolor='none', lw=0.5, edgecolor='gray'))
plt.show()