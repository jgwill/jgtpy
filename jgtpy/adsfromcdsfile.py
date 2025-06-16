"""Create ADS charts from cached CDS data.

This module exposes the ``adsfromcds`` entry point used to generate
plots directly from a CDS cache directory. Run ``adsfromcds --help``
for command details.
"""

import os
import pandas as pd
import JGTADS
from JGTADSRequest import JGTADSRequest
import argparse


from jgtutils.jgtos import ensure_directory_exists
from jgtutils.jgtcommon import new_parser, parse_args,add_instrument_timeframe_arguments

from JGTChartConfig import JGTChartConfig

def create_plot(i, t, cds_cache_path=None,cache_file_suffix="_cds_cache",chart_ns="charts",chart_outdir=None,chart_ext="png",feature_plot=1,chart_suffix="",override_path=None):
    # Determine the base directory and construct the CSV path
    if cds_cache_path is None:
      cds_cache_path=os.getenv("JGT_CACHE","/var/lib/jgt/cache/fdb_scanners")
      if not os.path.exists(cds_cache_path):
        #HOME/.cache/jgt/fdb_scanners
        cds_cache_path=os.path.expanduser("~/.cache/jgt/fdb_scanners")
    
    base_dir = cds_cache_path
    ifn=i.replace("/","-")
    tfn=t if t != "m1" else "mi1"
    fn= f"{ifn}_{tfn}{cache_file_suffix}.csv"
    spath = _mkfn(base_dir, fn)
    
    if not os.path.exists(spath) and override_path is None:
        base_dir = "."
        spath = _mkfn(base_dir, fn)
    elif override_path is not None:
        spath=override_path
        if not os.path.exists(spath):
            raise FileNotFoundError(f"File not found: {spath}")
    

    # Read the CSV file into a DataFrame
    df = pd.read_csv(spath, parse_dates=True, index_col=0)

    # Construct the path for saving additional figures
    if chart_outdir is not None or chart_outdir=="" or chart_outdir==".":
        chart_outdir=os.getcwd()
    chart_dir = os.path.join(chart_outdir, chart_ns, ifn)
    ensure_directory_exists(chart_dir)
    print("Chart directory:",chart_dir)
    
    save_additional_figures_path = os.path.join(chart_dir,f"{tfn}{chart_suffix}.{chart_ext}")

    # Create a JGTADSRequest object
    rq = JGTADSRequest.new_feature_plot(instrument=i, timeframe=t,feature_plot=feature_plot, save_additional_figures_path=save_additional_figures_path)
    #cc:JGTChartConfig=JGTChartConfig.new_feature_plot(feature_plot)
    # cc.show_feature_one_plot=True if feature_plot==1 else False
    # cc.show_feature_two_plot=True if feature_plot==2 else False
    # cc.show_feature_2403_plot=True if feature_plot==3 else False

    # Create the plot
    fig, _, _ = JGTADS.plot_from_cds_df(df, rq=rq, show=False)

    return fig

def _mkfn(base_dir, fn):
    return f"{base_dir}/{fn}"

def main():
    APP_DESCRIPTION = "Create a plot from CDS cache data."
    parser = new_parser(APP_DESCRIPTION,add_exiting_quietly_flag=True)
    parser=add_instrument_timeframe_arguments(parser,from_jgt_env=True,exclude_env_alias=False)
    parser.add_argument("-cp","--cache-path", type=str, help="The path to the CDS cache directory.")
    #cache_file_suffix
    parser.add_argument("--cache-file-suffix", type=str, help="The suffix for the cache file.",default="_cds_cache")
    #chart_ns
    parser.add_argument("--chart-ns", type=str, help="The namespace for the chart.",default="charts")
    #chart_outdir
    parser.add_argument("--chart-outdir", type=str, help="The output directory for the chart.",default=".")
    parser.add_argument("--chart-ext", type=str, help="The extension for the chart file.",default="png")
    #feature_plot
    parser.add_argument("-P","--feature-plot", type=int, help="The feature plot to show.",default=1)
    #chart_suffix
    parser.add_argument("-sx","--chart-suffix", type=str, help="The suffix for the chart file.",default="")
    #override_path
    parser.add_argument("-op","--override-path", type=str, help="The path to the CDS cache file to use.",default=None)

    args = parse_args(parser)

    create_plot(args.instrument, args.timeframe, args.cache_path, args.cache_file_suffix, args.chart_ns, args.chart_outdir, args.chart_ext, args.feature_plot, args.chart_suffix, args.override_path)

if __name__ == "__main__":
    main()