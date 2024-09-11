#!/usr/bin/env python

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

def _parse_args():
  parser=jgtcommon.new_parser("PDS File 2 CDS File","create CDS from an input PDS file","pds2cds")
  jgtcommon.add_input_file_argument(parser,add_f_alias=True)
  jgtcommon.add_output_argument(parser)
  jgtcommon.add_bars_amount_V2_arguments(parser)
  args=jgtcommon.parse_args(parser)
  return args

def convert_pds_2_cds(pdsfile,cdsfile_out=None,quotescount=-1):
  if not os.path.exists(pdsfile):
    #add .csv to support without extension
    pdsfile=pdsfile+".csv"
  if not os.path.exists(pdsfile):
    print("Error: File not found: "+pdsfile)
    from jgtutils.jgterrorcodes import JGTFILES_EXIT_ERROR_CODE
    exit(JGTFILES_EXIT_ERROR_CODE)
  df=pd.read_csv(pdsfile,index_col=0,parse_dates=True)
  if quotescount>0:
    df=df.tail(quotescount+609)
  cdsfile=cdsfile_out if cdsfile_out else pdsfile.replace(".csv",".cds.csv")
  cdf=cds.createFromDF(df)
  cdf.to_csv(cdsfile)
  return cdsfile

def main():
  args=_parse_args()
  convert_pds_2_cds(args.input_file,args.output,args.quotescount)
  
if __name__ == "__main__":
  main()
  