class Setting:
    def __init__(self, degree, duration, horizontal_unit=97, vertical_unit=56, sampling_frequency=1000,
                 display_width=195, display_height=113, resolution=1400, distance_to_screen=450):
        self.horizontal_unit = horizontal_unit
        self.vertical_unit = vertical_unit
        self.degree = degree
        self.duration = duration
        self.sampling_frequency = sampling_frequency
        self.pixel_width = display_width / resolution
        self.pixel_height = display_height / resolution
        self.resolution = resolution
        self.distance_to_screen = distance_to_screen

    def get_threshold(self):
        return self.degree * (self.horizontal_unit + self.vertical_unit)

    def get_window_size(self):
        return int(self.duration * self.sampling_frequency)
