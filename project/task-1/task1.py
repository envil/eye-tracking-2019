import csv
import numpy as np
from pathlib import Path
from setting import Setting
from idt import detect_fixations
import matplotlib.pyplot as plt

base_path = Path(__file__).parent
file_path = (base_path / '../data/train.csv').resolve()
subjects = ['s7', 's17', 's27', 's3', 's13', 's23']


def plot_fixations(index, info, data, fixation_centroids, setting):
    plt.figure(dpi=150)
    plt.plot(data[:, 0], data[:, 1], zorder=1)
    plt.plot(fixation_centroids[:, 0], fixation_centroids[:, 1], c='r', linewidth=0.5, zorder=2)
    plt.scatter(fixation_centroids[:, 0], fixation_centroids[:, 1], c='r', s=30, zorder=3)
    plt.title('({}) Subject: {}, Known = {}, Degree = {}, Duration = {}'.format(index, info[0], info[1], setting.degree, setting.duration))
    plt.savefig('./figures/setting2/{}.svg'.format(index))
    # plt.show()


def task1(setting):
    with file_path.open() as file:
        data = []
        test_info = []
        results = []
        i = 0
        for row in csv.reader(file, delimiter=','):
            if row[0] in subjects:
                test_info.append((row[0], row[1] == 'true'))
                row = np.array(row[2:])
                row = row.astype(np.float)
                data.append(np.reshape(row, (int(row.shape[0] / 2), 2)))
                fixation_centroids, fixation_time = detect_fixations(data[-1], setting.sampling_frequency, setting.get_window_size(),
                                                         setting.get_threshold())

                plot_fixations(i, test_info[-1], data[-1], fixation_centroids, setting)
                i += 1

    # fixation_centroids, fixation_time = detect_fixations(data[0], setting.sampling_frequency,
    #                                                      setting.get_window_size(),
    #                                                      setting.get_threshold())
    # plot_fixations(test_info[0], data[0], fixation_centroids, setting)
    # print(fixation_time)
    # print(fixation_centroids)


# setting1 = Setting(1, 0.03)
# task1(setting1)
# setting2 = Setting(1, 0.1)
# task1(setting2)
# setting3 = Setting(2, 0.03)
# task1(setting3)
setting4 = Setting(2, 0.1)
task1(setting4)
