import datetime as dt
import pandas as pd
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


from datetime import datetime

from JGTChartConfig import JGTChartConfig

from jgtutils.jgtos import create_filestore_path, mk_fn, mk_fn_range, mk_fullpath

import JGTPDSP as pds
df_cache={}
def getPH_crop(instrument:str,
               timeframe:str,
               dt_crop_last,
               quote_count:int=-1,
               quiet:bool=True               
          ):
    # Get the crop of the price history for the given instrument and timeframe
    key = instrument + "_" + timeframe + "_" + str(dt_crop_last)
    if key in df_cache:
          df=df_cache[key]
    else:
          df= pds.getPH_crop(instrument, timeframe, dt_crop_last, quote_count, quiet)
    # We will want to cache the a FULL readings of the price history OR WE WILL DO IT WITH THE CDS....
    return df

def getPH(instrument:str, timeframe:str, quote_count:int=-1, start=None, end=None, with_index=True, quiet:bool=True,convert_date_index_to_dt:bool=True,cc: JGTChartConfig=None,get_them_all:bool=False,use_full:bool=False,
          dt_crop_last=None,
          tlid_range=None,
    run_jgtfxcli_on_error=True,
    use_fresh=False,
    use_fresh_error_ignore=False
          ):
    # Get the price history for the given instrument and timeframe
    global df_cache
    df=pds.getPH(instrument, timeframe, quote_count, start, end, with_index, quiet,convert_date_index_to_dt,cc,get_them_all,use_full,dt_crop_last,tlid_range,run_jgtfxcli_on_error,use_fresh,use_fresh_error_ignore)
    # We will want to cache the a FULL readings of the price history OR WE WILL DO IT WITH THE CDS....
    return df

