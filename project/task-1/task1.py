import csv
import numpy as np
from pathlib import Path
from setting import Setting
from idt import detect_fixations
import matplotlib.pyplot as plt

base_path = Path(__file__).parent
file_path = (base_path / '../data/train.csv').resolve()
subjects = ['s7', 's17', 's27', 's3', 's13', 's23']


def task1(setting):
    with file_path.open() as file:
        data = []
        test_info = []
        for row in csv.reader(file, delimiter=','):
            if row[0] in subjects:
                test_info.append((row[0], row[1] == 'true'))
                row = np.array(row[2:])
                row = row.astype(np.float)
                data.append(np.reshape(row, (int(row.shape[0] / 2), 2)))

    print(data[0].shape)

    fixation_centroids, fixation_time = detect_fixations(data[0], setting.sampling_frequency, setting.get_window_size(),
                                                         setting.get_threshold())
    # print(fixation_time)
    # print(fixation_centroids)
    plt.plot(fixation_centroids[:, 0], fixation_centroids[:, 1], c='r')
    plt.plot(data[0][:, 0], data[0][:, 1])
    plt.show()


setting1 = Setting(1, 0.03)
setting2 = Setting(1, 0.1)
setting3 = Setting(2, 0.03)
setting4 = Setting(2, 0.1)
task1(setting1)
task1(setting2)
task1(setting3)
task1(setting4)
