import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
__author__ = 'gpamfilis'


class Particles(object):
    """
        TODO:
        
        1. have the program automatically find the start, end, and step of the time array. (regex?)
        2. have the program automatically find the dimension. (qx, qy and qz?) (regex?)
        3. specify dimensional direction.

    """
    def __init__(self, data_file, time_start=0, time_end=100, time_step=0.01, dimension=2, data_rows='all'):

        self.data_file = data_file  # the name of the data file (.txt)
        # read the data. ignore the first two 9 rows and get straight to the data. drop the 0th column because it
        # contains the particle id. the particle id can be referenced from the index of the data_frame.

        # import all the data
        if data_rows == 'all':
            self.data = pd.read_csv(self.data_file, skiprows=9, header=None, delim_whitespace=True).drop(0, axis=1)
        # check if an integer was provided. if so read up to those rows.
        elif isinstance(data_rows, int):
            self.data = pd.read_csv(self.data_file, nrows=data_rows, skiprows=9, header=None,
                                    delim_whitespace=True).drop(0, axis=1)
        else:
            pass

        # create the time array.
        # TODO: have this be done automatically.
        self.time = np.arange(time_start, time_end + time_step, time_step)

        # rename the columns from 0 to the size of the data_frame on axis=1 (columns) in order to drop them accordingly
        self.data.columns = range(0, self.data.shape[1])

        if dimension == 1:
            self.qx = self.data
            self.qx.columns = range(self.qx.shape[1])

        # if the dimension is set to 2 simply split the data into two arrays.
        elif dimension == 2:
            self.qx = self.data.drop(range(1, self.data.shape[1], 2), axis=1)
            self.qy = self.data.drop(range(0, self.data.shape[1], 2), axis=1)
            self.qx.columns = range(self.qx.shape[1])
            self.qy.columns = range(self.qy.shape[1])

        # TODO: add this option for the future also.
        elif dimension == 3:
            pass

        else:
            pass

    def particle_distribution(self, cut_line, time, particle_position_df, drop_returns='False'):

        """
        The question this method answers are two:
            1. CUMULATIVE
                what is the TOTAL number of particles that passed by the slice at L for every time period.
                Note: the output is cumulative. meaning that at time t_n the particle count includes all those
                before t_n-1 and

            2. DISCRETE
                How many particles pass at different times from the slice L.

        :param cut_line: float
        :param time: array
        :param particle_position_df:
        :param drop_returns: bool
        :return: dataframe

        drop_returns:
            if True:
                This simply means to drop the particles that dispersed backwards at any point in time
                to avoid a negative y axis in the discrete distribution curve.
        """

        # set up the particle array with three columns. time-cumulative-discrete.
        particle_array = np.zeros((time.shape[0], 3))
        particle_array[:, 0] = time
        print(time.shape)

        # cumulative case
        particle_array[:, 1] = self.cumulative_distribution(cut_line, particle_position_df)

        # discrete case
        for i in range(time.shape[0]-1):
            particle_array[i+1, 2] = particle_array[i+1, 1] - particle_array[i, 1]

        particle_distributions_df = pd.DataFrame(particle_array, columns=['time', 'cumulative', 'discrete'])

        return particle_distributions_df

    @staticmethod
    def cumulative_distribution(cut_line, particle_position_df):
        return (particle_position_df >= cut_line).sum(axis=1)


if __name__ == '__main__':
    p = Particles('./data/position_data_example_1.txt', dimension=2, time_start=0, time_end=500000, time_step=100)
    c = p.cumulative_distribution(50, p.qx)
    # dist = p.particle_distribution(100, p.time, p.qx)
    print(c)

    plt.plot(c)
    plt.show()