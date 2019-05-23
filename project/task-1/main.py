import csv
import numpy as np
from pathlib import Path
from setting import Setting
from result import Result
from idt import detect_fixations
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import utils

base_path = Path(__file__).parent
file_path = (base_path / '../data/train.csv').resolve()
subjects = ['s7', 's17', 's27', 's3', 's13', 's23', 'all']


# Task 1
def plot_fixations(index, info, data, fixation_centroids, setting, save_fig=False):
    plt.figure(dpi=150)
    plt.plot(data[:, 0], data[:, 1], zorder=1)
    plt.plot(fixation_centroids[:, 0], fixation_centroids[:, 1], c='r', linewidth=0.5, zorder=2)
    plt.scatter(fixation_centroids[:, 0], fixation_centroids[:, 1], c='r', s=30, zorder=3)
    plt.title('({}) Subject: {}, Known = {}, Degree = {}, Duration = {}'.format(index, info[0], info[1], setting.degree,
                                                                                setting.duration))
    if save_fig:
        plt.savefig('./figures/{}.svg'.format(index))
    plt.show()


def task2(results):
    print('sid\tknown\tmfd\t\tmfd_sd\tmsa\t\tmsa_sd')
    for subject in subjects:
        print(results[subject]['true'])
        print(results[subject]['false'])


def task3(results):
    with open('./output/group7.csv', 'w+') as out:
        out.write(
            'subject_id,MFD_true,MFD_SD_true,MFD_false,MFD_SD_false,MSA_true,MSA_SD_true,MSA_false,MSA_SD_false,MFD_overall,MFD_overall_SD,MSA_overall,MSA_overall_SD\r\n')
        for subject in subjects[:-1]:
            true_data = results[subject]['true']
            false_data = results[subject]['false']
            params = []
            params.append(subject)
            params.append(true_data.get_mfd())
            params.append(true_data.get_mfd_sd())
            params.append(false_data.get_mfd())
            params.append(false_data.get_mfd_sd())
            params.append(true_data.get_msa())
            params.append(true_data.get_msa_sd())
            params.append(false_data.get_msa())
            params.append(false_data.get_msa_sd())

            overall_result = Result('overall', None)
            overall_result.append_fixation_duration(true_data.fixation_durations)
            overall_result.append_fixation_duration(false_data.fixation_durations)
            overall_result.append_saccade_amplitude(true_data.saccade_amplitudes)
            overall_result.append_saccade_amplitude(false_data.saccade_amplitudes)
            params.append(overall_result.get_mfd())
            params.append(overall_result.get_mfd_sd())
            params.append(overall_result.get_msa())
            params.append(overall_result.get_msa_sd())
            out.write('{},{},{},{},{},{},{},{},{},{},{},{},{}\r\n'.format(*params))


def task4(results, save_fig=False):
    for subject in subjects:
        plot_stat(results[subject]['true'], save_fig)
        plot_stat(results[subject]['false'], save_fig)


def plot_stat(data, save_fig=False):
    plot_hist('MFD', data.fixation_durations, data.name, data.known, data.get_mfd(), data.get_mfd_sd(), save_fig)
    plot_hist('MSA', data.saccade_amplitudes, data.name, data.known, data.get_msa(), data.get_msa_sd(), save_fig)


def plot_hist(chart_name, data, name, known, mean, sd, save_fig=False):
    plt.figure(dpi=150)
    plt.hist(data, color='c')
    plt.title('{} {} {} Mean = {:.2f} SD = {:.2f}'.format(chart_name, name, known, mean, sd))
    ax = plt.gca()
    l0 = mlines.Line2D([mean, mean], [0, 100000], color='k', linestyle='--',
                       label='Mean')
    l1 = mlines.Line2D([mean - sd, mean - sd],
                       [0, 100000], color='red', linestyle='--',
                       label='SD')
    l2 = mlines.Line2D([mean + sd, mean + sd],
                       [0, 100000], color='red', linestyle='--',
                       label='SD')
    ax.add_line(l0)
    ax.add_line(l1)
    ax.add_line(l2)
    ax.legend(loc=1)
    if save_fig:
        plt.savefig('./figures/stats/{}-{}-{}.svg'.format(name, chart_name, known))
    plt.show()


def main(setting):
    with file_path.open() as file:
        data = []
        test_info = []
        results = {'all': {'true': Result('all', 'false'), 'false': Result('all', 'false')}}
        for subject in subjects:
            results[subject] = {'true': Result(subject, True), 'false': Result(subject, False)}
        i = 0
        for row in csv.reader(file, delimiter=','):
            if row[0] in subjects:
                [subject, known] = row[:2]
                test_info.append((subject, known == 'true'))
                row = np.array(row[2:])
                row = row.astype(np.float)
                data.append(np.reshape(row, (int(row.shape[0] / 2), 2)))
                fixation_centroids, fixation_time = detect_fixations(data[-1], setting.sampling_frequency,
                                                                     setting.get_window_size(),
                                                                     setting.get_threshold())

                results['all'][known].append_fixation_duration((fixation_time[:, 1] - fixation_time[:, 0]).tolist())
                results['all'][known].append_saccade_amplitude(
                    [utils.saccade_amplitude(setting, fixation_centroids[i] - fixation_centroids[i - 1]) for i in
                     range(1, fixation_centroids.shape[0])])

                results[subject][known].append_fixation_duration((fixation_time[:, 1] - fixation_time[:, 0]).tolist())
                results[subject][known].append_saccade_amplitude(
                    [utils.saccade_amplitude(setting, fixation_centroids[i] - fixation_centroids[i - 1]) for i in
                     range(1, fixation_centroids.shape[0])])

                # Task 1
                plot_fixations(i, test_info[-1], data[-1], fixation_centroids, setting, save_fig=False)
                # i += 1

    # Task 2
    task2(results)

    # Task 3
    task3(results)

    # Task 4
    task4(results, save_fig=False)


# setting1 = Setting(1, 0.03)
# task1(setting1)
setting2 = Setting(1, 0.1)
main(setting2)
# setting3 = Setting(2, 0.03)
# task1(setting3)
# setting4 = Setting(2, 0.1)
# task1(setting4)
