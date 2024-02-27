class JGTIDSRequest:
    """
    Represents a JGT IDS (Indicator Data Structure) request.

    Args:
        AOF (bool): Flag indicating whether to include AOF (AO Peak V1 (Would be replaced by the scipy.signals peak)) data.
        BigAlligator (bool): Flag indicating whether to include Big Alligator data.
        MFI (bool): Flag indicating whether to include MFI (Money Flow Index) data.
        GatorOscillator (bool): Flag indicating whether to include Gator Oscillator data.
        balligator_period_jaws (int): Period for the jaws line of the Alligator indicator.
        balligator_period_teeth (int): Period for the teeth line of the Alligator indicator.
        balligator_period_lips (int): Period for the lips line of the Alligator indicator.
        balligator_shift_jaws (int): Shift for the jaws line of the Alligator indicator.
        balligator_shift_teeth (int): Shift for the teeth line of the Alligator indicator.
        balligator_shift_lips (int): Shift for the lips line of the Alligator indicator.
        largest_fractal_period (int): Period for identifying the largest fractal.

    Attributes:
        AOF (bool): Flag indicating whether to include AOF
        BigAlligator (bool): Flag indicating whether to include Big Alligator data.
        MFI (bool): Flag indicating whether to include MFI (Market Facilitation Index) data.
        GatorOscillator (bool): Flag indicating whether to include Gator Oscillator data.
        balligator_period_jaws (int): Period for the jaws line of the Alligator indicator.
        balligator_period_teeth (int): Period for the teeth line of the Alligator indicator.
        balligator_period_lips (int): Period for the lips line of the Alligator indicator.
        balligator_shift_jaws (int): Shift for the jaws line of the Alligator indicator.
        balligator_shift_teeth (int): Shift for the teeth line of the Alligator indicator.
        balligator_shift_lips (int): Shift for the lips line of the Alligator indicator.
        largest_fractal_period (int): Period for identifying the largest fractal.
    """
    def __init__(self, AOF=False, BigAlligator=False, MFI=False, GatorOscillator=False,
                 balligator_period_jaws=89, balligator_period_teeth=55, balligator_period_lips=34,
                 balligator_shift_jaws=55, balligator_shift_teeth=34, balligator_shift_lips=21,
                 largest_fractal_period=89):
        self.AOF = AOF
        self.BigAlligator = BigAlligator
        self.MFI = MFI
        self.GatorOscillator = GatorOscillator
        self.balligator_period_jaws = balligator_period_jaws
        self.balligator_period_teeth = balligator_period_teeth
        self.balligator_period_lips = balligator_period_lips
        self.balligator_shift_jaws = balligator_shift_jaws
        self.balligator_shift_teeth = balligator_shift_teeth
        self.balligator_shift_lips = balligator_shift_lips
        self.largest_fractal_period = largest_fractal_period

