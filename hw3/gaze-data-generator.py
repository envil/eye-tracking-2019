import math
import sys
import json
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt

NO_OF_TARGET_POINTS = 6
DISPERSION_ANGLE_RANGE = [0.5, 2]  # holmquist_chpt5 P152
POISSON_LAMBDA = 200  # (ms) holmquist_chpt5


# Credit to gmb zre 11/1/07
def pix2angle(display, pix):
    pix_size = display.size / display.resolution.X  # cm/pix
    sz = pix * pix_size
    return 2 * 180 * math.atan(sz / (2 * display.distance)) / math.pi


# Credit to gmb zre 11/1/07
def angle2pix(display, ang):
    pix_size = display.size / display.resolution.X  # cm/pix
    sz = 2 * display.distance * math.tan(math.pi * ang / (2 * 180))  # cm
    return round(sz / pix_size)


# https://stackoverflow.com/a/22367889/1589218
def bound(low, high, value):
    return max(low, min(high, value))


# generate 6 random points on the screen to simulate the gaze
def generate_target_points(display):
    return np.array([generate_random_point([0, display.resolution.X], [0, display.resolution.Y]) for x in
                     range(NO_OF_TARGET_POINTS)])


def generate_random_point(x_range, y_range):
    return [np.random.randint(*x_range),
            np.random.randint(*y_range)]


def generate_fixation(config, point, dispersion_radius):
    current_fixation_duration = bound(config.fixation.min, config.fixation.max, np.random.poisson(POISSON_LAMBDA))
    print(current_fixation_duration)
    number_of_points = round(config.sam_freq * current_fixation_duration / 1000)
    x_range = [max(0, point[0] - dispersion_radius),
               min(config.display.resolution.X, point[0] + dispersion_radius)]
    y_range = [max(0, point[1] - dispersion_radius),
               min(config.display.resolution.Y, point[1] + dispersion_radius)]
    return [generate_random_point(x_range, y_range) for i in range(number_of_points)]


def generate_gaze_data(config):
    # first random point
    sequences = np.array([generate_random_point([0, config.display.resolution.X], [0, config.display.resolution.Y])])
    dispersion_radius = round(angle2pix(config.display, DISPERSION_ANGLE_RANGE[1]) / 2)

    target_points = generate_target_points(config.display)
    for point in target_points:
        sequences = np.concatenate((sequences, generate_fixation(config, point, dispersion_radius)))
        # generate saccade

    print(sequences.shape)
    # sequences = np.array(sequences)
    plt.scatter(target_points[:, 0], target_points[:, 1], c='r')
    plt.scatter(sequences[:, 0], sequences[:, 1], c='b', s=1)
    plt.show()


# fd_min=100 fd_max=250 sd_min=20 sd_max=50 vel_min=30 vel_max=100 sam_freq=50 X=1024 Y=768 distance=60 size=53.34
def main():
    file_path = sys.argv[1:][0]
    if file_path:
        with open(file_path, 'r') as f:
            config = json.load(f, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    generate_gaze_data(config)


if __name__ == '__main__':
    main()
