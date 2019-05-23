import math
import numpy as np


def saccade_amplitude(setting, distance_vector):
    distance = np.linalg.norm(
        np.array([distance_vector[0] * setting.pixel_width, distance_vector[1] * setting.pixel_height]))
    return 2 * math.degrees(math.atan(distance / (2 * setting.distance_to_screen)))
