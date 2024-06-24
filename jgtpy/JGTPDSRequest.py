import sys
import os
import json


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTBaseRequest import JGTBaseRequest
from jgtutils import jgtconstants as c


class JGTPDSRequest(JGTBaseRequest):
    def __init__(
        self,
        instrument: str = "",
        timeframe: str = "",
        timeframes=None,
        crop_last_dt: str = None,
        use_fresh: bool = False,
        use_full=False,
        keep_bid_ask=True,
        quotescount=300,  # @a Migrate to Use TODO
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.instrument = instrument
        self.timeframe = timeframe
        self.crop_last_dt = crop_last_dt
        self.use_full = use_full
        self.use_fresh = use_fresh
        self.quotescount = quotescount
        self.keep_bid_ask = keep_bid_ask
        if self.crop_last_dt is not None:
            print("-self.crop_last_dt is not None-")
            self.use_full = True
            self.use_fresh = False

        self.__timeframes__(timeframes)
    
    # create JGTPDSRequest from args (argparse) considering the super has the same method
    @staticmethod
    def from_args(args):
        return JGTPDSRequest(
            instrument=args.instrument,
            timeframe=args.timeframe,
            timeframes=args.timeframes if args.timeframes else None,
            crop_last_dt=args.crop_last_dt if args.crop_last_dt else None,
            use_fresh=args.fresh if args.fresh else False,
            use_full=args.full if args.full else False,
            keep_bid_ask=False if args.rmbidask else True,
            quotescount=args.quotescount if args.quotescount else 300,
        )
    
    def __timeframes__(self, timeframes=None):
        if isinstance(timeframes, list):
            self.timeframes = timeframes
        else:
            if timeframes == "default" or timeframes == "all" or timeframes is None:
                self.timeframes = os.getenv("T", "M1,W1,D1,H8,H4").split(",")
            else:
                self.timeframes = timeframes.split(",")

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

    # def __str__(self) -> str:
    #     return super().__str__() + f"instrument: {self.instrument}\n" + f"timeframe: {self.timeframe}\n" + f"timeframes: {self.timeframes if self.timeframes is not None else 'None'}\n" + f"crop_last_dt: {self.crop_last_dt if self.crop_last_dt is not None else 'None'}\n" + f"use_fresh: {self.use_fresh}\n" + f"use_full: {self.use_full}\n"
