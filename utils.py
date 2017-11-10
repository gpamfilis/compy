import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
__author__ = 'gpamfilis'


class Graphs:
    """
    This class provides us with a set of graphing tools in order to interpret our positional data and to make visual 
    inferences about the evolution of the moments in time.
    """
    def __init__(self):
        pass

    @staticmethod
    def plume_velocity_ratio(time, mom1x, dp_particle_diam, v_ave=0.000001, min_index=0, max_index=30, save_loc='v_ratio'):
        """
        This method computes the ratio of the plume average velocity over the fluid average velocity.
        It does this by finding the slope between the first normalized spatial moment versus time.
        
        :param time:
        :param mom1x: 
        :param dp_particle_diam: 
        :param v_ave: #(m/s)(1000mm/1m)(60s/1min) # this velocity is found at the line where the particles are on
        :param max_index: 
        :param min_index:
        :return: list
        """

        v_ave = v_ave*1000*60

        v_ratio = []
        for m1 in mom1x:
            slope, intercept, r_value, p_value, std_err = stats.linregress(time[min_index:max_index], m1[min_index:max_index])
            print(r_value**2)
            v_ratio.append(slope/v_ave)

        slope, intercept, r_value, p_value, std_err = stats.linregress(v_ratio, dp_particle_diam)

        line = []

        for d in dp_particle_diam:

            y_val = (slope * d) + intercept
            line.append(y_val)

        plt.title("Velocity Ratio versus Particle Diameter", fontsize=30)

        plt.plot(dp_particle_diam[:len(mom1x)], v_ratio)
        # plt.plot(dp_particle_diam, line)

        plt.ylabel('ylabel', fontsize=26)
        plt.xlabel('xlabel', fontsize=26)
        plt.ylabel(r"$\frac{\hat{V}_{plume}}{\hat{V}_{fluid}}$ [-]")
        plt.xlabel("$d_p$ [nm]")
        plt.grid()
        plt.savefig(save_loc)
        return v_ratio, line

    @staticmethod
    def first_moment_shading(mom1x, files, time, lower_limit=20, upper_limit=50, time_limit=100, legend_font_size=10):
        """
        This method shades the graph of the first normalized spatial moment versus time. The shading is defined by the
        limits: lower and upper. The purpose of this graph is to show what values where used in producing the velocity
        ratio graph.
        
        :param mom1x: 
        :param files: 
        :param time: 
        :param lower_limit: 
        :param upper_limit: 
        :param time_limit: 
        :param legend_font_size: 
        :return: None
        """
        m1x = pd.DataFrame(mom1x[:]).T
        m1x.columns = files
        m1x.index = time
        m1x.iloc[:time_limit].plot()
        # m1x[m1x.loc[:,:]<100].plot()
        plt.title('M1x-normalized versus time', fontsize=30)
        plt.ylabel(r"$M_{1,x}$ [mm]", fontsize=26)
        plt.xlabel("time [min]", fontsize=26)
        plt.grid()
        plt.legend(fontsize=legend_font_size)
        plt.axvline(time[lower_limit])
        plt.axvline(time[upper_limit])
        plt.fill_between(time, 0, 100, where=(time >= time[lower_limit]) & (time <= time[upper_limit]), facecolor='green', alpha=0.5)
        plt.savefig('./images/M1x-normalized-shading')


if __name__ == '__main__':
    pass
