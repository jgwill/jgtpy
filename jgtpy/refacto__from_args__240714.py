
import json
import JGTBaseRequest,JGTIDSRequest,JGTPDSRequest,JGTCDSRequest



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
    #jgtcommon.add_tlid_date_V2_arguments(parser)
    #jgtcommon.add_max_bars_arguments(parser)
    # jgtcommon.add_output_argument(parser)
    # jgtfxcommon.add_quiet_argument(parser)
    jgtcommon.add_verbose_argument(parser)
    jgtcommon.add_ads_argument(parser)
    #jgtcommon.add_use_full_argument(parser)
    jgtcommon.add_bars_amount_V2_arguments(parser)
    jgtcommon.add_use_fresh_argument(parser)
    
    jgtcommon.add_ids_mfi_argument(parser)
    jgtcommon.add_ids_gator_oscillator_argument(parser)
    jgtcommon.add_ids_balligator_argument(parser)
    jgtcommon.add_ids_talligator_argument(parser)
    jgtcommon.add_ids_fractal_largest_period_argument(parser)
    jgtcommon.add_viewpath_argument(parser)
    
    #dropna_volume
    jgtcommon.add_dropna_volume_argument(parser)
    jgtcommon.add_load_json_file_argument(parser)
    jgtcommon.add_jgtclirqdata_arguments(parser)
    
    jgtcommon.add_keepbidask_argument(parser)
    
    # print("Action groups:")
    # for g in parser._action_groups:
    #     print(g.__dict__)
    
    args=jgtcommon.parse_args(parser)
    # jgtcommon.add_cds_argument(parser)
    
    return args

_IDS_RQ_JSON_SAMPLE01="""
{
  "use_full": true,
  "use_fresh": false,
  "mfi_flag": true,
  "balligator_flag": true,
  "talligator_flag": true,
  "dropna_volume": true
}
"""

def main():
    cc = JGTChartConfig()
    args = parse_args()
    #print(args)
    #print(args.__dict__)
    #rq=JGTIDSRequest.JGTIDSRequest.from_args(args)
    #rq=JGTPDSRequest.JGTPDSRequest.from_args(args)
    #print("Pdsrq=",rq) 
    test_jgtbase=False
    if test_jgtbase:
      rq=JGTBaseRequest.JGTBaseRequest.from_args(args)
      #print("baserq=",rq) 
      print(rq.to_json())
      
    test_jgtpds=False
    if test_jgtpds:
      rq=JGTPDSRequest.JGTPDSRequest.from_args(args)
      print(rq.to_json())
      
    test_jgtids=False
    if test_jgtids:
      rq=JGTIDSRequest.JGTIDSRequest.from_args(args)
      print(rq.to_json())
    
    test_jgtids3=True
    if test_jgtids3:
      rq=JGTIDSRequest.JGTIDSRequest.from_args(args)
      rq.__from_json__(_IDS_RQ_JSON_SAMPLE01)
      print(rq.to_json())
    
    # test_jgtids2=True
    # if test_jgtids2:
    #   print(args.json_file)
    #   rq=JGTIDSRequest.JGTIDSRequest.from_(args.json_file)
    #   print(rq.to_json())
    #   sys.exit(0)
    #   rq=JGTIDSRequest.JGTIDSRequest.from_args(args)
    
    test_jgtids_from_json=False
    if test_jgtids_from_json:
      json_sample_file_path="samples/JGTIDSRequest_c1000_ba_ta_mfi.json"
      rq=JGTIDSRequest.JGTIDSRequest.from_json_file(json_sample_file_path)
        
      #rq=JGTIDSRequest.JGTIDSRequest.from_args(args)
      print(rq)
      
      
    test_jgtcds=False
    if test_jgtcds:
      rq=JGTCDSRequest.JGTCDSRequest.from_args(args)
      print(rq.to_json())
    sys.exit(0)
    
    


if __name__ == "__main__":
    main()
