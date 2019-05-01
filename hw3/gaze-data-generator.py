import math
import sys
import json
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt

NO_OF_TARGET_POINTS = 6
DISPERSION_ANGLE_RANGE = [0.5, 2]  # holmquist_chpt5 P152
MEAN_FIXATION_DURATION = 200  # (ms) mean duration of fixation holmquist_chpt5


# Credit to gmb zre 11/1/07, ported to python by Viet Ta
def pix2angle(display, pix):
    pix_size = display.size / display.resolution.X  # cm/pix
    sz = pix * pix_size
    return 2 * math.degrees(math.atan(sz / (2 * display.distance)))


# Credit to gmb zre 11/1/07, ported to python by Viet Ta
def angle2pix(display, ang):
    pix_size = display.size / display.resolution.X  # cm/pix
    sz = 2 * display.distance * math.tan(math.radians(ang / 2))  # cm
    return round(sz / pix_size)


# https://stackoverflow.com/a/22367889/1589218
def bound(low, high, value):
    return max(low, min(high, value))


# generate 6 random points on the screen to simulate the gaze
def generate_target_points(display):
    return np.array([generate_random_point([0, display.resolution.X], [0, display.resolution.Y]) for i in
                     range(NO_OF_TARGET_POINTS)])


def generate_random_point(x_range, y_range):
    return [np.random.randint(*x_range),
            np.random.randint(*y_range)]


def decide_next_point(previous_point_index, index_range):
    next_point_index = previous_point_index
    while next_point_index == previous_point_index:
        next_point_index = np.random.randint(*index_range)
    return next_point_index


def generate_fixation(config, point, dispersion_radius):
    fixation_duration = bound(config.fixation.min, config.fixation.max,
                              np.random.poisson(MEAN_FIXATION_DURATION))
    number_of_points = round(config.sam_freq * fixation_duration / 1000)
    x_range = [bound(0, config.display.resolution.X, point[0] - dispersion_radius),
               bound(0, config.display.resolution.X, point[0] + dispersion_radius)]
    y_range = [bound(0, config.display.resolution.Y, point[1] - dispersion_radius),
               bound(0, config.display.resolution.Y, point[1] + dispersion_radius)]
    return [generate_random_point(x_range, y_range) for i in range(number_of_points)]


def generate_saccade(config, point_a, point_b):
    speed = np.random.randint(config.velocity.min, config.velocity.max)
    point_distance = pix2angle(config.display, np.linalg.norm(point_a - point_b))
    duration = bound(config.saccade.min, config.saccade.max, 1000 * point_distance / speed)

    number_of_point_between = int(duration * config.sam_freq / 1000)
    x_sequence = np.linspace(point_a[0], point_b[0], number_of_point_between + 2, dtype=int)
    y_sequence = np.linspace(point_a[1], point_b[1], number_of_point_between + 2, dtype=int)
    return np.array(list(zip(x_sequence[1:-1], y_sequence[1:-1])))


def generate_gaze_data(config):
    # first random point on the screen
    sequences = np.array([generate_random_point([0, config.display.resolution.X], [0, config.display.resolution.Y])])
    dispersion_radius = round(angle2pix(config.display, DISPERSION_ANGLE_RANGE[1]) / 2)

    # generate target points to gaze
    target_points = generate_target_points(config.display)

    # generate the gaze data, fixations and saccades occupy alternatively for simplification
    previous_point = sequences[0]
    previous_point_index = -1
    while sequences.shape[0] < 150:
        current_point_index = decide_next_point(previous_point_index, [0, len(target_points)])
        current_point = target_points[current_point_index]
        sequences = np.concatenate((sequences, generate_saccade(config, previous_point, current_point)))
        sequences = np.concatenate((sequences, generate_fixation(config, current_point, dispersion_radius)))
        previous_point_index = current_point_index
        previous_point = sequences[-1]

    # trim data
    sequences = sequences[:150]
    # add noise
    sequences += np.random.randint(-10, 10, sequences.shape)
    sequences[:, 0] = np.clip(sequences[:, 0], 0, config.display.resolution.X)
    sequences[:, 1] = np.clip(sequences[:, 1], 0, config.display.resolution.Y)

    # plotting the data
    plt.plot(sequences[:, 0], sequences[:, 1], c='y', zorder=1)
    plt.scatter(sequences[:, 0], sequences[:, 1], c='b', s=10, zorder=2)
    plt.scatter(target_points[:, 0], target_points[:, 1], c='r', s=100, zorder=3)
    plt.show()

    # writing the data to the csv file
    with open('output.csv', 'w+') as f:
        f.write('X,Y\r\n')
        for line in sequences:
            f.write('{},{}\r\n'.format(*line))


def main():
    file_path = sys.argv[1:][0]
    if file_path:
        with open(file_path, 'r') as f:
            config = json.load(f, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    generate_gaze_data(config)


if __name__ == '__main__':
    main()
