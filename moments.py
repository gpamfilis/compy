import os
import particles
import numpy as np
import pandas as pd


# import matplotlib.pyplot as plt
# the saving format is as follows: /seed_#/xy_dp.txt

data_directory = '/Users/georgepamfilis/Dropbox/THESIS/comsol_project/DATA/micromodel/geomentry_v0/'


def get_seeds(directory):
    seeds = [int(a.split('_')[1]) for a in os.listdir(directory)]
    return seeds


def get_data_paths(directory, seeds):
    particle_data_file = []
    for seed in seeds:
        pos = os.listdir(directory+'seed_'+str(seed))
        particle_data_file.append([directory+'seed_'+str(seed)+'/'+p for p in pos if '.DS_Store' not in p])
    empty = {}
    for i, seed in enumerate(seeds):
        empty[str(seed)] = particle_data_file[i]
    return empty


def zero_moment(pos):
    m0 = []
    for i in range(pos.shape[1]):
        x_data = pos[i]
        particles_in_media = ((x_data >= 0) & (x_data != np.nan) & (x_data < .1)).sum()
        m0.append(particles_in_media)
    return m0


def mom(n, position, time, m0, norm=True):
    mn = np.zeros(time.shape[0])
    for i in range(position.shape[1]):
        if m0[i] == 0:
            print("no more particles in the media for moment_{1} [m^{1}] @ time = {0} [min]".format(time[i], n))
            print("")
            mn[i] = 0
        else:
            mn[i] = np.sum(position[i]**n)
    if norm:
        return mn/m0
    else:
        return mn


def zero_moment_compute_and_save(seeds, paths, time, files):
    for f, file_ in enumerate(files):
        m0s = []
        for s, seed in enumerate(seeds):
            fil = paths[str(seed)][f]
            print(file_.split('/')[-1])
            par = particles.Particles(fil, dimension=2, time_start=0, time_end=4, time_step=500)
            m0 = zero_moment(par.qx)
            m0s.append(m0)
        df = pd.DataFrame(np.array(m0s).T, columns=[str(s) for s in seeds], index=time)
        df.to_csv('/Users/georgepamfilis/Dropbox/THESIS/comsol_project/DATA/micromodel/data/m0/' + file_.split('/')[-1])


def nth_moment_compute_and_save(nth, seeds, paths, time, files):\

    # todo: create mnx,mny directories
    print('X-DIRECTION')
    for f, file_ in enumerate(files):
        mnxs = []
        for s, seed in enumerate(seeds):
            fil = paths[str(seed)][f]
            print(file_.split('/')[-1])
            par = particles.Particles(fil, dimension=2, time_start=0, time_end=4, time_step=500)
            x = par.qx[par.qx < 0.1]
            m0 = zero_moment(par.qx)
            mnx = mom(nth, position=x, time=time, m0=m0, norm=True)
            mnxs.append(mnx)
        df = pd.DataFrame(np.array(mnxs).T, columns=[str(s) for s in seeds], index=time)
        df.to_csv('/Users/georgepamfilis/Dropbox/THESIS/comsol_project/DATA/micromodel/data/m'+str(nth)+'x/' +
                  file_.split('/')[-1])
    print('Y-DIRECTION')
    for f, file_ in enumerate(files):
        mnys = []
        for s, seed in enumerate(seeds):
            fil = paths[str(seed)][f]
            print(file_.split('/')[-1])
            par = particles.Particles(fil, dimension=2, time_start=0, time_end=4, time_step=500)
            y = par.qy[par.qx < 0.1]
            m0 = zero_moment(par.qx)
            mny = mom(nth, position=y, time=time, m0=m0, norm=True)
            mnys.append(mny)
        df = pd.DataFrame(np.array(mnys).T, columns=[str(s) for s in seeds], index=time)
        df.to_csv('/Users/georgepamfilis/Dropbox/THESIS/comsol_project/DATA/micromodel/data/m'+str(nth)+'y/' +
                  file_.split('/')[-1])


if __name__ == '__main__':
    seeds = get_seeds(data_directory)
    paths = get_data_paths(data_directory, seeds)
    time = np.arange(0, 4 + 1 / 500., 1 / 500.)
    files = paths['100']
    zero_moment_compute_and_save(seeds, paths, time, files)
    nth_moment_compute_and_save(1, seeds, paths, time, files)
    nth_moment_compute_and_save(2, seeds, paths, time, files)
