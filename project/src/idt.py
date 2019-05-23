import numpy as np


def calculate_dispersion(points):
    X = points[:, 0]
    Y = points[:, 1]
    return (np.max(X) - np.min(X)) + (np.max(Y) - np.min(Y))


def detect_fixations(data, sampling_frequence, window_size, dispersion_threshold):
    fixation_centroids = []
    fixation_time = []
    start = 0
    expansion = window_size
    while start + expansion < data.shape[0]:
        D = calculate_dispersion(data[start:start + expansion, :])

        if D > dispersion_threshold:
            start += 1
        else:
            expansion += 1
            while D <= dispersion_threshold and start + expansion < data.shape[0]:
                D = calculate_dispersion(data[start:start + expansion, :])
                expansion += 1

            fixation_centroids.append(np.mean(data[start:start + expansion], axis=0))
            fixation_time.append([start / sampling_frequence, (start + expansion - 1) / sampling_frequence])
            start = start + expansion
            expansion = window_size

    return np.array(fixation_centroids), np.array(fixation_time)
