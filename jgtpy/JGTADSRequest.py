
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTCDSRequest import JGTCDSRequest


class JGTADSRequest(JGTCDSRequest):
    def __init__(self, *args, plot_ao_peaks=True, show=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.plot_ao_peaks = plot_ao_peaks
        self.show = show
        #self.big_alligator_flag = big_alligator_flag
        self.plot_ao_peaks = plot_ao_peaks
        #self.big_alligator_flag = big_alligator_flag
        
