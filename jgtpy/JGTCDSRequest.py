
import sys
import os
import json


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTIDSRequest import JGTIDSRequest

class JGTCDSRequest(JGTIDSRequest):
    def __init__(self,cds_notes=None, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.cds_notes = cds_notes
        
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=2)
    
    def __from_args__(self, args):
        #print("CDS __from_args__")
        super().__from_args__(args)
        if hasattr(args, 'cds_notes'):
            self.cds_notes = args.cds_notes
        
    @staticmethod
    def from_args(args):
        # if hasattr(args, 'json_content'):
        #     rq = JGTCDSRequest.from_json(args.json_content)
        #     return rq
        
        instance = JGTCDSRequest()
        instance.__from_args__(args)
        
        return instance
    
        # return JGTCDSRequest(
        #     instrument=args.instrument,
        #     timeframe=args.timeframe,
        #     quotescount=args.quotescount,
        #     viewpath=args.viewpath,
        #     use_fresh=args.fresh,
        #     use_full=args.full,
        #     gator_oscillator_flag=args.gator_oscillator_flag,
        #     mfi_flag=args.mfi_flag,
        #     balligator_flag=args.balligator_flag,
        #     balligator_period_jaws=args.balligator_period_jaws,
        #     largest_fractal_period=args.largest_fractal_period,
        #     talligator_flag=args.talligator_flag,
        #     talligator_period_jaws=args.talligator_period_jaws,
        #     verbose_level=args.verbose
        # )
    # def __str__(self) -> str:
    #     return super().__str__() + f"dummy_cds_flag: {self.dummy_cds_flag}\n" 
