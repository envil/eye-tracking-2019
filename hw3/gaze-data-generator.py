import math
import sys
import json
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt

NO_OF_TARGET_POINTS = 6


class Display:
    def __init__(self, dist, width, resolution):
        self.dist = dist
        self.width = width
        self.resolution = resolution


# Credit to gmb zre 11/1/07
def pix2angle(display, pix):
    pix_size = display.width / display.resolution.X  # cm/pix
    sz = pix * pix_size
    return 2 * 180 * math.atan(sz / (2 * display.dist)) / math.pi


# Credit to gmb zre 11/1/07
def angle2pix(display, ang):
    pix_size = display.width / display.resolution.X  # cm/pix
    sz = 2 * display.dist * math.tan(math.pi * ang / (2 * 180))  # cm
    return round(sz / pix_size)


# generate 6 random points on the screen to simulate the gaze
def generate_target_points(display):
    return np.array([np.random.randint(0, display.resolution.X, NO_OF_TARGET_POINTS),
                     np.random.randint(0, display.resolution.Y, NO_OF_TARGET_POINTS)])


def generate_gaze_data(config):
    target_points = generate_target_points(config.display)
    plt.scatter(target_points[0], target_points[1])
    plt.show()


# fd_min=100 fd_max=250 sd_min=20 sd_max=50 vel_min=30 vel_max=100 sam_freq=50 X=1024 Y=768 dist=60 size=53.34
def main():
    file_path = sys.argv[1:][0]
    if file_path:
        with open(file_path, 'r') as f:
            config = json.load(f, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    generate_gaze_data(config)


if __name__ == '__main__':
    main()
