#!/usr/bin/env python

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# import .

from jgtutils import (
    jgtconstants as constants,
    jgtcommon as jgtcommon,
    jgtwslhelper as wsl,
)
import argparse
import JGTPDSP as pds
import JGTCDS as cds
import JGTADS as ads
from JGTChartConfig import JGTChartConfig


import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(description="Process command parameters.")
    # jgtfxcommon.add_main_arguments(parser)
    jgtcommon.add_instrument_timeframe_arguments(parser)
    jgtcommon.add_date_arguments(parser)
    jgtcommon.add_tlid_range_argument(parser)
    jgtcommon.add_max_bars_arguments(parser)
    # jgtcommon.add_output_argument(parser)
    # jgtfxcommon.add_quiet_argument(parser)
    jgtcommon.add_verbose_argument(parser)
    jgtcommon.add_ads_argument(parser)
    jgtcommon.add_use_full_argument(parser)
    jgtcommon.add_use_fresh_argument(parser)
    
    # jgtcommon.add_cds_argument(parser)
    args = parser.parse_args()
    return args


def main():
    cc = JGTChartConfig()
    args = parse_args()
    instrument = args.instrument
    timeframe = args.timeframe
    quotes_count = args.quotescount
    cc.nb_bar_on_chart = quotes_count
    
    verbose_level = args.verbose
    quiet = False
    if verbose_level == 0:
        quiet = True
    
    full = False
    fresh = False
    if args.fresh:
        fresh=True
    
    if args.full:
        full = True

    date_from = None
    date_to = None
    tlid_range = None
    if args.tlidrange:
        # @STCGoal Get range prices from cache or request new
        tlid_range = args.tlidrange
        print("#FUTURE Support for tlid range")
        tmpcmd = wsl._mkbash_cmd_string_jgtfxcli_range(
            instrument, timeframe, tlid_range,verbose_level=verbose_level,
            use_full=full
        )
        print(tmpcmd)
        print("#-----------Stay tune -------- Quitting for now")
        return

    if args.datefrom:
        date_from = args.datefrom.replace("/", ".")
    if args.dateto:
        date_to = args.dateto.replace("/", ".")

    show_ads = False
    if args.ads:
        show_ads = True

    # process_cds=args.cds
    process_cds = True
    # output=False
    # compress=False

    # print("Verbose level : " + str(verbose_level))
    if process_cds:
        print("Processing CDS")
        output = True
    # if args.compress:
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

        print_quiet(quiet, "Getting for : " + instrument + "_" + timeframe)
        instruments = instrument.split(",")
        timeframes = timeframe.split(",")

        for instrument in instruments:
            for timeframe in timeframes:
                createCDS_for_main(
                    instrument,
                    timeframe,
                    quiet=quiet,
                    verbose_level=verbose_level,
                    tlid_range=tlid_range,
                    show_ads=show_ads,
                    cc=cc,
                    use_full=full,
                    use_fresh=fresh
                )
                # else:
                #     p = pds.getPH(instrument, timeframe, quotes_count, date_from, date_to, False, quiet)
                #     if verbose_level > 0:
                #         print(p)

    except Exception as e:
        jgtcommon.print_exception(e)

    # try:
    #    jgtpy.off()
    # except Exception as e:
    #    jgtfxcommon.print_exception(e)


# if __name__ == "__main__":
#     main()

# print("")
# #input("Done! Press enter key to exit\n")


def createCDS_for_main(
    instrument,
    timeframe,
    quiet,
    verbose_level=0,
    tlid_range=None,
    show_ads=False,
    cc: JGTChartConfig = None,
    use_full=False,
    use_fresh=False,
):
    # implementation goes here
    col2remove = constants.columns_to_remove
    config = jgtcommon.readconfig()
    if "columns_to_remove" in config:  # read it from config otherwise
        col2remove = config["columns_to_remove"]
    quietting = True
    if verbose_level > 1:
        quietting = False
        
    try:
        #cdspath, cdf = cds.createFromPDSFileToCDSFile(
        cdspath, cdf = cds.createFromPDSFileToCDSFile(
            instrument, 
            timeframe, 
            quiet=quietting,
            #cc=cc,
            use_full=use_full,
            use_fresh=use_fresh,
            columns_to_remove=col2remove,
        )  # @STCIssue: This is not supporting -c NB_BARS_TO_PROCESS, should it ?
        
        print_quiet(quiet, cdspath)
        print_quiet(quiet, cdf)
    except Exception as e:
        print("Failed to create CDS for : " + instrument + "_" + timeframe)
        print("jgtcli::Exception: " + str(e))
        
    try:
        if (
            show_ads
        ):  # (data,instrument,timeframe,nb_bar_on_chart = 375,show=True,plot_ao_peaks=False)
            ads.plot_from_cds_df(
                cdf, instrument, timeframe, show=True, plot_ao_peaks=True, cc=cc
            )
    except Exception as e:
        print("ADS Failed to plot CDS for : " + instrument + "_" + timeframe)
        print("jgtcli::ADS::Exception: " + str(e))

def print_quiet(quiet, content):
    if not quiet:
        print(content)


if __name__ == "__main__":
    main()
