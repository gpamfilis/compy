__author__ = 'gpamfilis'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('data/output.txt')

data_d = data[data.discrete != 0]
data_c = data[data.cumulative !=0]
if __name__ == '__main__':
    plt.scatter(data_d['time'], data_d['discrete'])
    #  plt.plot(data_c['time'], data_c['cumulative'])

    plt.xlabel('time')
    plt.ylabel('N')
    plt.grid(1)
    plt.show()

