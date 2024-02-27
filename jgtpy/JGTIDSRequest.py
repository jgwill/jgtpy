class JGTIDSRequest:
    def __init__(self, AOF=False, BigAlligator=False, MFI=False):
        self.AOF = AOF
        self.BigAlligator = BigAlligator
        self.MFI = MFI
        
        self.GatorOscillator=False
        
        self.balligator_period_jaws = 89
        self.balligator_period_teeth = 55
        self.balligator_period_lips = 34
        self.balligator_shift_jaws = 55
        self.balligator_shift_teeth = 34
        self.balligator_shift_lips = 21
        
        self.largest_fractal_period = 89
