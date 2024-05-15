#import JGTCDS as cds

#todo expose only the required functions to run CDS

## Requirement:   

"""
* Generate the CDS to file
* --@STCIssue Parse the CDS and get Valid signal (not fully implemented)

"""

import warnings

# Ignore FutureWarning
warnings.simplefilter(action="ignore", category=FutureWarning)

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTCDSRequest import JGTCDSRequest


def createCDSRequestFromArgs(args, instrument, timeframe):
    rq = JGTCDSRequest()
    rq.instrument = instrument
    rq.keep_bid_ask = args.keepbidask
    rq.timeframe = timeframe
    rq.quotescount = args.quotescount
    rq.use_fresh = args.fresh if args.fresh else False
    rq.use_full = args.full if args.full else False
    rq.gator_oscillator_flag = (
        args.gator_oscillator_flag if args.gator_oscillator_flag else False
    )
    rq.mfi_flag = args.mfi_flag if args.mfi_flag else False
    rq.balligator_flag = args.balligator_flag if args.balligator_flag else False
    rq.balligator_period_jaws = args.balligator_period_jaws
    rq.largest_fractal_period = args.largest_fractal_period
    rq.verbose_level = args.verbose
    return rq
