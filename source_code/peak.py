class Peak:
    def __init__(self, label='Si 111', d_spacing=3.345, d_min=3., d_max=3.5):
        """
        defining the  diffraction peak class

        Parameters
        ----------
        label: string
            label of the peak
        d_spacing: float
            d-spacing value of the peak
        d_min: float
            minimum value of the range of the d_spacing value
        d_max: float
            minimum value of the range of the d_spacing value
        """
        self.label = label
        self.d_spacing = d_spacing
        self.dmin = d_min
        self.dmax = d_max


