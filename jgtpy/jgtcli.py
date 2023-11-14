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
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    instrument = args.i
    timeframe = args.timeframe
    quotes_count = args.quotescount
    date_from = args.datefrom
    date_to = args.dateto
    output = args.output

    try:
        print("Getting for : " + instrument + "_" + timeframe)
        p=pds.getPH(instrument,timeframe)
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
