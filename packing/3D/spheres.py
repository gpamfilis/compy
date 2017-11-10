import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# http://demonstrations.wolfram.com/CirclesPackedInACircle/
__author__ = 'George Pamfilis'

def rotate_around_origin(r,angle):
    # http://tutorial.math.lamar.edu/Classes/CalcII/PolarCoordinates.aspx
    x = r * np.cos(angle)
    y = r * np.sin(angle)
    return x, y, 0, 0


def packing_attempt_1():
    r = 1
    r_cylinder = 1
    p1 = (0, 0)
    ps = [p1]
    angle = 60
    # first layer
    for i in range(6):
        p_new = rotate_around_origin(2 * r + (r / 2) * 0, np.deg2rad(angle))
        ps.append(p_new)
        angle += 60

    # second layer
    angle = 30
    for i in range(6):
        p_new = rotate_around_origin(3 * r + (r / 2) * 1, np.deg2rad(angle))
        ps.append(p_new)
        angle += 60
    angle = 60
    for i in range(6):
        p_new = rotate_around_origin(4 * r + (r / 2) * 0, np.deg2rad(angle))
        ps.append(p_new)
        angle += 60
    angle = 60 + 30 / 2 + 4
    for i in range(6):
        p_new = rotate_around_origin(5 * r + (r / 3), np.deg2rad(angle))
        ps.append(p_new)
        angle += 60
    angle = 60 + 30 / 2 + 4 - 8 + 30
    for i in range(6):
        p_new = rotate_around_origin(5 * r + (r / 3), np.deg2rad(angle))
        ps.append(p_new)
        angle += 60
    angle = 60
    for i in range(6):
        p_new = rotate_around_origin(5 * r + (r / 1) * 1, np.deg2rad(angle))
        ps.append(p_new)
        angle += 60
    angle = 30
    for i in range(6):
        p_new = rotate_around_origin(6 * r + (r / 1) * 1, np.deg2rad(angle))
        ps.append(p_new)
        angle += 60
    angle = 60 + 13.75
    for i in range(6):
        p_new = rotate_around_origin(6 * r + (r / 1) * 1 + r / 4, np.deg2rad(angle))
        ps.append(p_new)
        angle += 60
    angle = 46.25
    for i in range(6):
        p_new = rotate_around_origin(6 * r + (r / 1) * 1 + r / 4, np.deg2rad(angle))
        ps.append(p_new)
        angle += 60
    angle = 60
    for i in range(6):
        p_new = rotate_around_origin(6 * r + (r / 1) * 1 + r / 4 + (r / 1.25), np.deg2rad(angle))
        ps.append(p_new)
        angle += 60
    plt.figure(figsize=(20, 20 * (1 / 1)))
    fig = plt.gcf()
    # circle1 = plt.Circle((0, 0), 6*r+r+r+r/2+r, color="r")
    circle1 = plt.Circle((0, 0), 6 * r + r + r + r, color="r")
    fig.gca().add_artist(circle1)
    for p in ps:
        circle1 = plt.Circle((p[0], p[1]), r)
        fig.gca().add_artist(circle1)
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.savefig('test2.png')
    plt.show()


def packing_attempt_2(layers=2, stack=5):

    r = 1
    r_cylinder = 1
    p1 = (0, 0, 0, 0)
    ps = [p1]
    angle = 60
    # first layer
    #
    for i in range(6):
        p_new = rotate_around_origin(2 * r + (r / 24), np.deg2rad(angle))
        ps.append(p_new)
        angle += 60

    for j in range(2, layers):
        if j ==2:
            angle = 60 + 30/j
        else:
            angle = 60 + 30/j

        for i in range(6*j):
            p_new = rotate_around_origin(j*r+r*j - (r/(j*6*2)), np.deg2rad(angle))
            ps.append(p_new)
            angle += 60/j


    #create stacking
    stacks = []
    slice = np.array(ps)
    #set radius
    slice[:, 3] = r

    for i in range(stack):
        slice_test = np.copy(slice)
        slice_test[:, 2] = i*2*r
        print(i*2*r)
        stacks.append(np.round(slice_test,5))

    all_stacks = np.concatenate(stacks, axis=0)
    print(all_stacks)
    pd.DataFrame(all_stacks).to_csv("packing.txt", index=None, header=["x","y","z","r"], sep="\t")


    plt.figure(figsize=(20, 20 * (1 / 1)))
    fig = plt.gcf()
    # circle1 = plt.Circle((0, 0), 6*r+r+r+r/2+r, color="r")
    circle1 = plt.Circle((0, 0), r*layers*2 - r, color="r")
    fig.gca().add_artist(circle1)
    for p in ps:
        circle1 = plt.Circle((p[0], p[1]), r)
        fig.gca().add_artist(circle1)
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.savefig('test2.png')
    plt.show()


if __name__ == '__main__':
    packing_attempt_2(layers=4)


