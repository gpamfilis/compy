# coding: utf-8

"""
Explain WTF your doing
"""

# import pandas as pd
# import scipy
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

import particles

plt.rcParams['figure.figsize'] = (20, 16)
plt.rcParams['xtick.labelsize'] = 'x-large'
plt.rcParams['ytick.labelsize'] = 'x-large'
__author__ = 'George Pamfilis'


seeds = [1, 100, 142, 200, 1344, 10000]
time = np.arange(0, 4, 1/500.)


def zero_moment(pos):
    m0 = []
    for t in range(pos.shape[1]):
        s = pos[t].dropna().shape[0]
        if s is None:
            m0.append(0)
        else:
            m0.append(s)
    return np.array(m0)


def mom(n, position, time, m0, norm=True):
    mn = np.zeros(time.shape[0])
    for i in range(position.shape[1]):
        if m0[i] == 0:
            print("no more particles in the media for moment_{1} [m^{1}] @ time = {0} [min]".format(time[i],n))
            print("")
            break
        else:
            mn[i] = np.sum(position[i]**n)
    if norm:
        return mn/m0
    else:
        return mn


dispersions_x = []
dispersions_y = []

for seed in seeds[:]:
    print 'seed: ', seed
    folder = '/Users/georgepamfilis/Dropbox/THESIS/comsol_project/DATA/micromodel/geomentry_v0/seed_' + str(seed)

    files = ["/xy_250.txt",
             "/xy_500.txt",
             "/xy_750.txt",
             "/xy_1000.txt",
             "/xy_1250.txt",
             "/xy_1500.txt",
             "/xy_1750.txt",
             "/xy_2000.txt"]

    d = [int(f.split('_')[1].split('.')[0]) for f in files]
    files_ = [folder + f for f in files]

    print('x-dir')

    spatial_variances_x = []

    for f in range(len(files_))[:]:

        print(files_[f])
        par = particles.Particles(files_[f], dimension=2, time_start=0, time_end=4, time_step=500)
        x = par.qx[par.qx < .1]
        y = par.qy[par.qx < .1]

        spa_var_x = []

        for t in range(x.shape[1]):
            a = x[t]
            a = a.dropna()
            if a.shape[0] == 0:
                spa_var_x.append(0)
            else:
                spa_var_x.append((np.sum(a ** 2) / a.shape[0]) - (np.sum(a ** 1) / a.shape[0]) ** 2)
        spatial_variances_x.append(spa_var_x)

    l, h = 200, 400

    disp_x = []

    for i in range(len(spatial_variances_x)):
        s = spatial_variances_x[i][l:h]
        slope, intercept, r_value, p_value, std_err = stats.linregress(time[l:h], s)
        print(r_value ** 2, slope / 2, intercept)
        disp_x.append(slope / 2)

    print('y-dir')

    spatial_variances_y = []

    for f in range(len(files_))[:]:
        print(files_[f])
        par = particles.Particles(files_[f], dimension=2, time_start=0, time_end=4, time_step=500)
        y = par.qy[par.qx < .1]
        spa_var_y = []
        for t in range(y.shape[1]):
            a = y[t]
            a = a.dropna()
            if a.shape[0] == 0:
                spa_var_y.append(0)
            else:
                spa_var_y.append((np.sum(a ** 2) / a.shape[0]) - (np.sum(a ** 1) / a.shape[0]) ** 2)

        spatial_variances_y.append(spa_var_y)

    disp_y = []

    for i in range(len(spatial_variances_y)):
        s = spatial_variances_y[i][l:h]
        slope, intercept, r_value, p_value, std_err = stats.linregress(time[l:h], s)
        print(r_value ** 2, slope / 2, intercept)
        disp_y.append(slope / 2)

    dispersions_x.append(disp_x)
    dispersions_y.append(disp_y)

if __name__ == '__main__':
    pass
