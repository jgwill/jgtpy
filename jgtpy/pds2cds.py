#!/usr/bin/env python
"""Convert a Price Data Service file to a Chaos Data Service file.

Exposes the ``pds2cds`` entry point. Run ``pds2cds --help`` for
command options.
"""

import sys
import os



sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# import .

from jgtutils import (
    jgtconstants as constants,
    jgtcommon as jgtcommon,
)

import JGTCDS as cds
import JGTCDSSvc as svc

import pandas as pd

epilog = """
Proto usage:JGTPY_DATA=/tmp/fds;

jgtfxcli -i EUR/USD -t m5 -c 12000;

tlid_v=2409022200;python jgtpy/pds2cds.py -f /tmp/fds/pds/EUR-USD_m5 -c 500 -to $tlid_v -o /tmp/fds/pds/EUR-USD_m5.$tlid_v.cds.csv;
wc -l /tmp/fds/pds/EUR-USD_m5.$tlid_v.cds.csv;
tail -n 1 /tmp/fds/pds/EUR-USD_m5.$tlid_v.cds.csv
"""
def _parse_args():
  parser=jgtcommon.new_parser("PDS File 2 CDS File",epilog,"pds2cds",add_exiting_quietly_flag=True)
  jgtcommon.add_input_file_argument(parser,add_f_alias=True)
  jgtcommon.add_output_argument(parser)
  jgtcommon.add_bars_amount_V2_arguments(parser)
  jgtcommon.add_tlid_date_to_argumments(parser)
  args=jgtcommon.parse_args(parser)
  return args

def convert_pds_2_cds(pdsfile,cdsfile_out=None,quotescount=-1,tlid_dateto=None,usual_cds_required_bars = 609):

  if not os.path.exists(pdsfile):
    #add .csv to support without extension
    pdsfile=pdsfile+".csv"
  if not os.path.exists(pdsfile):
    print("Error: File not found: "+pdsfile)
    from jgtutils.jgterrorcodes import JGTFILES_EXIT_ERROR_CODE
    exit(JGTFILES_EXIT_ERROR_CODE)
  df=pd.read_csv(pdsfile,index_col=0,parse_dates=True)
  if tlid_dateto:
    df=df.loc[:tlid_dateto]
  if quotescount>0:    
    df=df.tail(quotescount+usual_cds_required_bars)
  cdsfile=cdsfile_out if cdsfile_out else pdsfile.replace(".csv",".cds.csv")
  cdf=cds.createFromDF(df)
  cdf.to_csv(cdsfile)
  return cdsfile

def main():
  args=_parse_args()
  convert_pds_2_cds(args.input_file,args.output,args.quotescount,args.tlid_dateto)
  
if __name__ == "__main__":
  main()
  