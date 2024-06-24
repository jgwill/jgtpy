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
import JGTCDSSvc as svc
import JGTADS as ads
from JGTChartConfig import JGTChartConfig

import  JGTADSRequest as RQ

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
    
    jgtcommon.add_ids_mfi_argument(parser)
    jgtcommon.add_ids_gator_oscillator_argument(parser)
    jgtcommon.add_ids_balligator_argument(parser)
    jgtcommon.add_ids_talligator_argument(parser)
    jgtcommon.add_ids_fractal_largest_period_argument(parser)
    jgtcommon.add_viewpath_argument(parser)
    
    # jgtcommon.add_cds_argument(parser)
    args = parser.parse_args()
    return args


def main():
    cc = JGTChartConfig()
    args = parse_args()

    gator_oscillator_flag = (
        args.gator_oscillator_flag if args.gator_oscillator_flag else False
    )
    mfi_flag = True #mfi_flag = args.mfi_flag if args.mfi_flag else False
    balligator_flag = args.balligator_flag if args.balligator_flag else False
    talligator_flag = args.talligator_flag if args.talligator_flag else False
    balligator_period_jaws = args.balligator_period_jaws
    talligator_period_jaws = args.talligator_period_jaws
    largest_fractal_period = args.largest_fractal_period


    viewpath=args.viewpath
    
    instrument = args.instrument
    timeframe = args.timeframe
    quotescount = args.quotescount
    #print("#@STCIssue : quotes_count is not passed , it should be !")
    cc.nb_bar_on_chart = quotescount
    
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
        if verbose_level > 0:print("Processing CDS")
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
                    use_fresh=fresh,
                    gator_oscillator_flag=gator_oscillator_flag,
                    mfi_flag=mfi_flag,
                    balligator_flag=balligator_flag,
                    balligator_period_jaws=balligator_period_jaws,
                    largest_fractal_period=largest_fractal_period,
                    talligator_flag=talligator_flag,
                    talligator_period_jaws=talligator_period_jaws,
                    viewpath=viewpath,
                    quotescount=quotescount
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
    use_fresh=True,
    gator_oscillator_flag=False,
    mfi_flag=True,
    balligator_flag=False,
    balligator_period_jaws=89,
    largest_fractal_period=89,
    talligator_flag=False,
    talligator_period_jaws=377,
    viewpath=False,
    quotescount=300,
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
            keep_bid_ask=True,
            gator_oscillator_flag=gator_oscillator_flag,
            mfi_flag=mfi_flag,
            balligator_flag=balligator_flag,
            balligator_period_jaws=balligator_period_jaws,
            largest_fractal_period=largest_fractal_period,
            talligator_flag=talligator_flag,
            talligator_period_jaws=talligator_period_jaws,
            viewpath=viewpath,
            quotescount=quotescount
        )  # @STCIssue: This is not supporting -c NB_BARS_TO_PROCESS, should it ?
        if cdspath is not None and cdf is None and viewpath:
            return #we printed it already.
        #@STCGoal GENERATE THE ZONE from the FRESH CDF
        #print("Zone updating...")
        fpath,zone_data = svc.zone_update_from_cdf(instrument,timeframe,cdf,quiet=quietting)
        print("    ",instrument," ",timeframe," zone: ",zone_data["zcol"].values[0])
        
        print_quiet(quiet, cdspath)
        print_quiet(quiet, cdf)
    except Exception as e:
        print("Failed to create CDS for : " + instrument + "_" + timeframe)
        print("jgtcli::Exception in cds.createFromPDSFileToCDSFile(: " + str(e))
        
    try:
        if (
            show_ads
        ):  # (data,instrument,timeframe,nb_bar_on_chart = 375,show=True,plot_ao_peaks=False)
            
            rq=RQ.JGTADSRequest()
            rq.instrument=instrument
            rq.timeframe=timeframe
            rq.show=True
            rq.cc=cc
            _chart,_arr,_data = ads.plot_v2(rq)
            #ads.plot_from_cds_df(
            #    cdf, instrument, timeframe, show=True, plot_ao_peaks=True, cc=cc
            #)
    except Exception as e:
        print("ADS Failed to plot CDS for : " + instrument + "_" + timeframe)
        print("jgtcli::ADS::Exception in  _chart,_arr,_data = ads.plot_v2(rq): " + str(e))

def print_quiet(quiet, content):
    if not quiet:
        print(content)


if __name__ == "__main__":
    main()
