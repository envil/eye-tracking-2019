import statistics as stat


class Result:
    def __init__(self, name, known):
        self.name = name
        self.known = known
        self.fixation_durations = []
        self.saccade_amplitudes = []

    def append_fixation_duration(self, data):
        self.fixation_durations.extend(data)

    def append_saccade_amplitude(self, data):
        self.saccade_amplitudes.extend(data)

    def get_mfd(self):
        return stat.mean(self.fixation_durations) if len(self.fixation_durations) > 0 else 0

    def get_msa(self):
        return stat.mean(self.saccade_amplitudes) if len(self.saccade_amplitudes) > 0 else 0

    def get_mfd_sd(self):
        return stat.stdev(self.fixation_durations) if len(self.fixation_durations) > 0 else 0

    def get_msa_sd(self):
        return stat.stdev(self.saccade_amplitudes) if len(self.saccade_amplitudes) > 0 else 0

    def __str__(self):
        return '{}\t{}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}'.format(self.name, self.known, self.get_mfd(), self.get_mfd_sd(),
                                                               self.get_msa(), self.get_msa_sd())
