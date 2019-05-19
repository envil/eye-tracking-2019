class Setting:
    def __init__(self, degree, duration, horizontal_unit=97, vertical_unit=56, sampling_frequency=1000):
        self.horizontal_unit = horizontal_unit
        self.vertical_unit = vertical_unit
        self.degree = degree
        self.duration = duration
        self.sampling_frequency = sampling_frequency

    def get_threshold(self):
        return self.degree * (self.horizontal_unit + self.vertical_unit)

    def get_window_size(self):
        return int(self.duration * self.sampling_frequency)
