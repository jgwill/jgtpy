

import sys
import os


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTBaseRequest import JGTBaseRequest


class JGTPDSRequest(JGTBaseRequest):
    def __init__(self, instrument:str="SPX500", timeframe:str="H4", crop_last_dt:str=None, use_fresh:bool=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instrument = instrument
        self.timeframe = timeframe
        self.crop_last_dt = crop_last_dt
        self.use_fresh = use_fresh
