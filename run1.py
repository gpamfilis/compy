from moments import SpatialMoments
import seaborn as sns
import matplotlib.pyplot as plt
__author__ = 'gpamfilis'

import particles


if __name__ == '__main__':
    # p = particles.Particles(data_file='./data/test.txt', dimension=1, time_start=0, time_end=10000, time_step=100)
    # print(p.qx)
    sp = SpatialMoments('./data/test.txt', dimension=1, time_start=0, time_end=10000, time_step=100)
    # print(sp.px.shape, sp.px[0].shape, sp.py.shape, sp.time.shape)
    mn = sp.spatial_moments(sp.px, sp.time, 1)
    # sns.jointplot(sp.time, mn, color="#4CB391", stat_func=None)
    # plt.savefig("test")
    # # print(sp.px)
