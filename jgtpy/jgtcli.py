import jgtpy
from jgtpy import jgtfxcommon
import argparse

from jgtpy import JGTPDS as pds

import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description='Process command parameters.')
    #jgtfxcommon.add_main_arguments(parser)
    jgtfxcommon.add_instrument_timeframe_arguments(parser)
    jgtfxcommon.add_date_arguments(parser)
    jgtfxcommon.add_max_bars_arguments(parser)
    jgtfxcommon.add_output_argument(parser)
    jgtfxcommon.add_quiet_argument(parser)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    instrument = args.i
    timeframe = args.timeframe
    quotes_count = args.quotescount
    date_from = args.datefrom
    date_to = args.dateto
    output=None
    compress=False
    quiet=False
    if args.compress:
        compress = args.compress
        output = True # in case
    if args.output:
        output = args.output

    try:
        if not quiet:
            print("Getting for : " + instrument + "_" + timeframe)
        if output :
            fpath=pds.getPH2file(instrument,timeframe,quotes_count,date_from,date_to,False,quiet,compress)
            if not quiet:
                print(fpath)
        else:
            p=pds.getPH(instrument,timeframe,quotes_count,date_from,date_to,False,quiet)
            if not quiet:
                print(p)
            
    except Exception as e:
        jgtfxcommon.print_exception(e)

    try:
        jgtpy.off()
    except Exception as e:
        jgtfxcommon.print_exception(e)

# if __name__ == "__main__":
#     main()

# print("")
# #input("Done! Press enter key to exit\n")
