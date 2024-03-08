
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTCDSRequest import JGTCDSRequest


class JGTADSRequest(JGTCDSRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.big_alligator_flag = big_alligator_flag
