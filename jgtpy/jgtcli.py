import jgtpy

from . import jgtconstants as constants
from . import jgtcommon as jgtcommon
import argparse

from . import JGTPDSP as pds

import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description='Process command parameters.')
    #jgtfxcommon.add_main_arguments(parser)
    jgtcommon.add_instrument_timeframe_arguments(parser)
    jgtcommon.add_date_arguments(parser)
    jgtcommon.add_max_bars_arguments(parser)
    #jgtcommon.add_output_argument(parser)
    #jgtfxcommon.add_quiet_argument(parser)
    jgtcommon.add_verbose_argument(parser)
    jgtcommon.add_cds_argument(parser)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    instrument = args.instrument
    timeframe = args.timeframe
    quotes_count = args.quotescount
    date_from = None
    date_to = None

    if args.datefrom:
        date_from = args.datefrom.replace('/', '.')
    if args.dateto:
        date_to = args.dateto.replace('/', '.')

    process_cds=args.cds
    #output=False
    #compress=False
    verbose_level = args.verbose
    quiet=False
    if verbose_level == 0:
        quiet=True
    #print("Verbose level : " + str(verbose_level))
    if process_cds:
        print("Processing CDS")
        output=True
    #if args.compress:
    #    compress = args.compress
    #     output = True # in case
    # if args.output:
    #     output = True

    if verbose_level > 1:
        if date_from:
            print("Date from : " + str(date_from))
        if date_to:
            print("Date to : " + str(date_to))


    try:
        
        print_quiet(quiet,"Getting for : " + instrument + "_" + timeframe)
        instruments = instrument.split(',')
        timeframes = timeframe.split(',')


        for instrument in instruments:
            for timeframe in timeframes:
                createCDS_for_main(instrument, timeframe, quiet, verbose_level)
                # else:
                #     p = pds.getPH(instrument, timeframe, quotes_count, date_from, date_to, False, quiet)
                #     if verbose_level > 0:
                #         print(p)
         
    except Exception as e:
        jgtcommon.print_exception(e)

    #try:
    #    jgtpy.off()
    #except Exception as e:
    #    jgtfxcommon.print_exception(e)

# if __name__ == "__main__":
#     main()

# print("")
# #input("Done! Press enter key to exit\n")

def createCDS_for_main(instrument, timeframe, quiet, verbose_level=0):
    # implementation goes here
    from jgtpy import JGTCDS as cds
    col2remove=constants.columns_to_remove
    config = jgtcommon.readconfig()
    if 'columns_to_remove' in config:  # read it from config otherwise
        col2remove = config['columns_to_remove']
    quietting=True
    if verbose_level> 1:
        quietting=False
    cdspath=cds.createFromPDSFileToCDSFile(instrument,timeframe,col2remove,quietting)
    print_quiet(quiet,cdspath)



def print_quiet(quiet,content):
    if not quiet:
        print(content)
