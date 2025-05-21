import argparse
import sys
import os
import json


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTBaseRequest import JGTBaseRequest
from jgtutils import jgtconstants as c
from jgtutils.jgtconstants import NB_BARS_BY_DEFAULT_IN_CDS

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
        quotescount=NB_BARS_BY_DEFAULT_IN_CDS,  # @a Migrate to Use TODO
        dropna_volume=True,
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
        self.dropna_volume = dropna_volume
        if self.timeframe=="M1":
            print("INFO(JGTPDSRequest): M1 timeframe detected, dropna_volume set to False")
            self.dropna_volume = False
        if self.crop_last_dt is not None:
            print("-self.crop_last_dt is not None-")
            self.use_full = True
            self.use_fresh = False

        self.__timeframes__(timeframes)
    
    
    # Set values from args
    def __from_args__(self, args: argparse.Namespace):
        super().__from_args__(args)
        self.instrument = args.instrument
        self.timeframe = args.timeframe
        self.crop_last_dt = args.crop_last_dt
        self.use_fresh = args.fresh
        self.use_full = args.full
        self.keep_bid_ask = args.keep_bid_ask
        self.quotescount = args.quotescount  
        self.dropna_volume = args.dropna_volume if args.dropna_volume else False
        self.__timeframes__(args.timeframes) 
        
    
    # create JGTPDSRequest from args (argparse) considering the super has the same method
    @staticmethod
    def from_args(args: argparse.Namespace):
        # if hasattr(args, 'json_content'):
        #     rq = JGTPDSRequest.from_json(args.json_content)
        #     return rq
        #print("INFO(JGTPDSRequest): from_args", args)
        instance=JGTPDSRequest()
        instance.__from_args__(args)
        
        return instance
        
        # return JGTPDSRequest(
        #     instrument=args.instrument,
        #     timeframe=args.timeframe,
        #     timeframes=args.timeframes if args.timeframes else None,
        #     crop_last_dt=args.crop_last_dt if args.crop_last_dt else None,
        #     use_fresh=args.fresh if args.fresh else False,
        #     use_full=args.full if args.full else False,
        #     keep_bid_ask=False if args.rmbidask else True,
        #     quotescount=args.quotescount if args.quotescount else 300,
        #     dropna_volume=args.dropna_volume or not args.dont_dropna_volume,
        # )
    
    def __timeframes__(self, timeframes=None):
        if isinstance(timeframes, list):
            self.timeframes = timeframes
        else:
            from jgtutils import jgtcommon
            if timeframes is not None:
                self.timeframes = jgtcommon.parse_timeframes_helper(timeframes)
            else:
                self.timeframes = jgtcommon.parse_timeframes_helper(self.timeframe) # So we get an array specified also in the timeframe
            # if timeframes == "default" or timeframes == "all" or timeframes is None:
            #     try:
            #         self.timeframes = os.getenv("T", "M1,W1,D1,H8,H4").split(",")
            #     except:
            #         self.timeframes = None
            # else:
            #     try:
            #         self.timeframes = timeframes.split(",")
            #     except:
            #         self.timeframes = None

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=2)
    
    @staticmethod
    def from_json(json_str):
        return json.loads(json_str)
    # def __str__(self) -> str:
    #     return super().__str__() + f"instrument: {self.instrument}\n" + f"timeframe: {self.timeframe}\n" + f"timeframes: {self.timeframes if self.timeframes is not None else 'None'}\n" + f"crop_last_dt: {self.crop_last_dt if self.crop_last_dt is not None else 'None'}\n" + f"use_fresh: {self.use_fresh}\n" + f"use_full: {self.use_full}\n"
