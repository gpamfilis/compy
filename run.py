
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from particles import Particles
from moments import Moments

__author__ = 'gpamfilis'


class Run:

    @staticmethod
    def run_temporal_moments_calculation(number_of_moments, segmentation_tuple, kind_of='not_norm'):
        p = Particles('./data/position_data_1_1.txt')
        segmentations = np.arange(*segmentation_tuple)
        moments_n = np.zeros((len(segmentations), number_of_moments))
        if kind_of == 'norm':
            mom = Moments.normalized_temporal_moment
        elif kind_of == 'not_norm':
            mom = Moments.temporal_moment
        for n in np.arange(0, number_of_moments):  # order of the moment
            for i, l in enumerate(segmentations):  # lengths to be tested
                moments_n[i, n] = mom(n, p.time, p.discrete_particle_distribution(l, p.time, p.qy))
                #   print(np.trapz(p.discrete_particle_distribution(l, p.time, p.qy)))
        moment_list = []
        for i in np.arange(0, number_of_moments):
            moment_list.append('m_'+str(i))
        moments_n_df = pd.DataFrame(moments_n, columns=moment_list, index=segmentations)
        moments_n_df.to_csv('./data/temporal_moments.csv')
        moments_n_df = moments_n_df.drop('m_0', axis=1)  # drop in order not to plot
        moments_n_df.plot()
        plt.xlabel('Segmentation L [m]')
        plt.xlim(segmentations[1], segmentations[-1])
        plt.ylabel('Moment []')
        plt.title('Moment versus L')
        plt.savefig('./data/temporal_moments.png')

    def run_particle_distibution_graphs(self):
        p = Particles('./data/position_data_example_1.txt', dimension=2, time_start=0, time_end=500000, time_step=100)
        dist_cum = p.cumulative_distribution(0.0000505, p.qx)
        # dist_disc = p.discrete_particle_distribution(0.00005, p.time, p.qy)

        plt.scatter(range(len(dist_cum)), dist_cum)
        plt.xlabel('time')
        plt.ylabel('N')
        plt.grid(1)
        plt.show()

if __name__ == '__main__':
    r = Run()
    #r.run_temporal_moments_calculation(5, (0, 0.0002, 0.00001))
    r.run_particle_distibution_graphs()
    #p = Particles('data/particle_position.txt')
    #print(Moments.temporal_moment(0, p.time, p.discrete_particle_distribution(0.00005, p.time, p.qy)))
    #plt.plot(p.time, p.discrete_particle_distribution(0.00005, p.time, p.qy))
    #plt.show()
    #print(len(p.time))
    #print(np.trapz(p.discrete_particle_distribution(0.00005, p.time, p.qy), dx=0.01))


