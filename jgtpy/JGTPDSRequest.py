import sys
import os


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTBaseRequest import JGTBaseRequest
from jgtutils import jgtconstants as c




class JGTPDSRequest(JGTBaseRequest):
    def __init__(
        self,
        instrument: str = "SPX500",
        timeframe: str = "H4",
        timeframes=None,
        crop_last_dt: str = None,
        use_fresh: bool = False,
        use_full=False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.instrument = instrument
        self.timeframe = timeframe

        self.crop_last_dt = crop_last_dt
        self.use_full = use_full
        self.use_fresh = use_fresh
        if self.crop_last_dt is not None:
            print("-self.crop_last_dt is not None-")
            self.use_full = True
            self.use_fresh = False

        self.__timeframes__(timeframes)
            

    def __timeframes__(self, timeframes=None):
        if isinstance(timeframes, list):
            self.timeframes = timeframes
        else:
            if timeframes == "default" or timeframes == "all" or timeframes is None:
                self.timeframes = os.getenv("T", "M1,W1,D1,H8,H4").split(",")
            else:
                self.timeframes = timeframes.split(",")

    # def __str__(self) -> str:
    #     return super().__str__() + f"instrument: {self.instrument}\n" + f"timeframe: {self.timeframe}\n" + f"timeframes: {self.timeframes if self.timeframes is not None else 'None'}\n" + f"crop_last_dt: {self.crop_last_dt if self.crop_last_dt is not None else 'None'}\n" + f"use_fresh: {self.use_fresh}\n" + f"use_full: {self.use_full}\n"
