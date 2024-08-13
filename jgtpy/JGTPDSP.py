
import datetime as dt
import pandas as pd
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import JGTPDHelper as jpd

from JGTConfig import local_fn_compression
from JGTPDHelper import *
from datetime import datetime
from jgtutils import jgtcommon,iprops,jgtos
from jgtutils import jgtos as jos
from jgtutils.jgtos import create_filestore_path, mk_fn, mk_fn_range, mk_fullpath
from jgtutils.jgtconstants import VOLUME
#from jgtutils.jgtconstants import (TJAW_PERIODS,TTEETH_PERIODS)

from JGTChartConfig import JGTChartConfig

from jgtutils import jgtwslhelper as wsl

renameColumns=True
addOhlc=True


cleanseOriginalColumns=True
useLocal=True

def refreshPH(instrument:str, timeframe:str,quote_count:int=-1, quiet:bool=True,use_full:bool=False,verbose_level=0,tlid_range=None,keep_bid_ask=False):
  #print debug information
  # print(f"Refreshing {instrument} {timeframe}")
  # print(f"quote_count: {quote_count}")
  # print(f"use_full: {use_full}")
  # print(f"verbose_level: {verbose_level}")
  # print(f"tlid_range: {tlid_range}")
  
  if not quiet:
    print(f"Refreshing {instrument} {timeframe}")
  try:
    wsl.getPH(instrument, timeframe,quote_count=quote_count, tlid_range=tlid_range, use_full=use_full,verbose_level=verbose_level,keep_bid_ask=keep_bid_ask)
  except Exception as e:
    print("Error in refreshPH")
    raise e

#df = df[df.index <= crop_last_dt]
df_full_cache = {}
def add_df_to_full_cache(instrument:str, timeframe:str, df,quiet:bool=True):
  global df_full_cache
  key = instrument + "_" + timeframe
  df_full_cache[key] = df

def _get_full_ph_from_cache_and_add(instrument:str, 
                          timeframe:str,
                          quiet:bool=True,
                          quote_count:int=-1,
                          dt_crop_last=None ):
  global df_full_cache
  key = instrument + "_" + timeframe
  
  if key not in df_full_cache:
    #df = getPH(instrument, timeframe, quiet=quiet, use_full=True)
    getPH_crop(instrument, timeframe,
                  dt_crop_last=dt_crop_last,
                  quote_count=quote_count,
                  quiet=quiet,
                  #use_full=True,
                  use_cache_full=True)
  return df_full_cache[key]

def getPH_crop_use_cache(instrument:str, 
                               timeframe:str, 
                               dt_crop_last, 
                               quote_count:int=-1, 
                               quiet:bool=True):
  
  df=_get_full_ph_from_cache_and_add(instrument, timeframe, quiet=quiet)
  selected = _if_crop_ph(dt_crop_last, df)
  return select_quote_count(quote_count, selected, quiet=quiet)


def getPH_crop(instrument:str,
               timeframe:str,
               dt_crop_last,
               quote_count:int=-1,
               quiet:bool=True,   
               use_cache_full=False
          ):
  global df_full_cache
  if not quiet:  
    print("getting cropped data....")
    print(" dt_crop_last: " + str(dt_crop_last))
    print(" quote_count: " + str(quote_count))
  
  
  df=getPH(instrument, timeframe, quiet=quiet,dt_crop_last=dt_crop_last,use_full=True,use_cache_full=use_cache_full)
  
  df = select_quote_count(quote_count, df, quiet=quiet)
  return df


def select_quote_count(quote_count, df, quiet=True):
    ldf = len(df)
    if  ldf > quote_count  and quote_count != -1:
      if not quiet:
        print("  we selected: " + str(quote_count) + " bars")
      selected = df.iloc[-quote_count:].copy()
    else:
      selected = df.copy()
    return selected
  

###################### CLEAN ME UP IF TALLIGATOR WORK >>>>>
# def get_talligator_required_quote_count(cc: JGTChartConfig,quote_count=-1):
#   TJAW_REQUIRED_CALC_BARS = TJAW_PERIODS+TTEETH_PERIODS
#   tmp = cc.nb_bar_on_chart
#   total = tmp + TJAW_REQUIRED_CALC_BARS
#   return total



def getPH(instrument:str, 
          timeframe:str, 
          quote_count:int=-1, 
          start=None, 
          end=None, 
          with_index=True, 
          quiet:bool=True,
          convert_date_index_to_dt:bool=True,
          cc: JGTChartConfig=None,
          get_them_all:bool=False,
          use_full:bool=False,
          dt_crop_last=None,
          tlid_range=None,
          run_jgtfxcli_on_error=True,
          use_fresh=False,
          use_fresh_error_ignore=False,   
          use_cache_full=False,
          keep_bid_ask=False,
          dropna_volume=True,
          #talligator_flag=False,
          ):
  global df_full_cache
  if use_cache_full:
    use_full=True
  
  #@STCissue quote_count is ignored or irrelevant in start/end
  #@a Adequate start and end from the stored file
  if cc is None:
    cc = JGTChartConfig()
    
  ###################### CLEAN ME UP IF TALLIGATOR WORK >>>>>
  _DEBUG_2406161729=True

  # if _DEBUG_2406161729:print("Quote count before fix and _get_ph_surely_fresh(2406161729): " + str(quote_count))
  
  
  # TALLIGATOR_REQUIRED_QUOTE_COUNT = get_talligator_required_quote_count(cc,quote_count)
  # #print cc.nb_bar_to_retrieve
  # if _DEBUG_2406161729:print("cc.nb_bar_to_retrieve: " + str(cc.nb_bar_to_retrieve))
  # if quote_count == -1 and use_full == False: #@STCIssue JGTChartConfig being Replaced by JGTPDSPRequest
  #   if _DEBUG_2406161729:print("NOT Usefull and quote_count == -1")
  #   fix_240325 = 50 if not talligator_flag else TALLIGATOR_REQUIRED_QUOTE_COUNT
  #   quote_count = cc.nb_bar_to_retrieve + fix_240325
  # # If we have the talligator_flag on, we require a certain amount of bars to calculate the indicator so we make sure we have enough data
  # if talligator_flag and quote_count < TALLIGATOR_REQUIRED_QUOTE_COUNT:
  #   quote_count = TALLIGATOR_REQUIRED_QUOTE_COUNT
    
  # # If we dont have enough data in full when using crop_last_dt, we should use fresh
  # if _DEBUG_2406161729:print("Quote count after if _get_ph_surely_fresh(2406161729): " + str(quote_count))
  # if _DEBUG_2406161729:exit(0)
  ###################### CLEAN ME UP IF TALLIGATOR WORK <<<<<
  
  df = _get_ph_surely_fresh(instrument, timeframe, quote_count, with_index, quiet, convert_date_index_to_dt, use_full, dt_crop_last, tlid_range, run_jgtfxcli_on_error, use_fresh_error_ignore, use_cache_full,use_fresh=use_fresh,keep_bid_ask=keep_bid_ask)
  
  
  df = if_select_start_end(df, start, end,quiet)
    
  
  df = _if_crop_ph(dt_crop_last, df)
      
  ldf = len(df)
  if ldf > quote_count and not get_them_all and quote_count > 50:
    if not use_full:
      df = df.iloc[-quote_count:]
  
  if dropna_volume and timeframe != "M1":
    if VOLUME in df.columns:
      df = df.dropna(subset=[VOLUME])
      #also drop where VOLUME is 0
      df = df[df[VOLUME] != 0]
  return df

def _get_ph_surely_fresh(instrument, timeframe, quote_count, with_index, quiet, convert_date_index_to_dt, use_full, dt_crop_last, tlid_range, run_jgtfxcli_on_error, use_fresh_error_ignore, use_cache_full,use_fresh=False,keep_bid_ask=False):
  use_UTC=False
  _dt_requirements = _get_dt_requirement_for_tf(timeframe,use_UTC) if dt_crop_last is None else dt_crop_last
  #@STCIssue Open: Sundays, between 5:00 and 5:15 pm EST. Close: Fridays, around 4:55 pm EST. Closed: Fridays 5:00 pm to Sunday 5:00 pm EST.
  #print("_dt_requirements: " + str(_dt_requirements)  + " dt_crop_last: " + str(dt_crop_last))
  
  # We are not using crop_last_dt neither full, we should use fresh anyways if our short stored data is not enough fresh
  # we will tel it our date is now
  #quiet=False
  our_data_is_ok=use_fresh
  if not use_fresh:
    print_quiet(quiet,"Checking if dt range has enough bars")
    our_data_is_ok=_check_if_dt_range_has_enough_bars(instrument, timeframe, _dt_requirements, quote_count, quiet,use_full=use_full)
  else:
    print_quiet(quiet,"We are using fresh, skipping checking if dt range has enough bars")
    
  if not our_data_is_ok:
    if not quiet:
      print("Our data is not ok, using fresh")
    use_fresh=True
  else:
    if not quiet:
      print("Our data is ok, not using fresh")
  

  

  if use_fresh:
    try:
      refreshPH(instrument, timeframe,quote_count=quote_count, tlid_range=tlid_range, use_full=use_full,verbose_level=1,keep_bid_ask=keep_bid_ask)
    except: #Raise ExceptionUseFreshData
      print("Error in getPH when using fresh")
      if use_fresh_error_ignore:
        pass      
      raise Exception("Error in getPH, use_fresh failed")
  
  df = getPH_from_filestore(instrument, timeframe, quiet, False, with_index,convert_date_index_to_dt,use_full=use_full,tlid_range=tlid_range)
  if df  is None and run_jgtfxcli_on_error:
    print_quiet(quiet,"NO DATA IN DF, running jgtfxcli")
  #df = getPH_from_filestore(instrument, timeframe, quiet, False, with_index,convert_date_index_to_dt,use_full=use_full)
  #@STCIssue its more PDSP that should run this logics
    try: 
      if run_jgtfxcli_on_error:
        print("Running jgtfxcli")
        refreshPH(instrument, timeframe,quote_count=quote_count, tlid_range=tlid_range, use_full=use_full,verbose_level=1,keep_bid_ask=keep_bid_ask)
      # CALL IT BACK AGAIN
        df = getPH_from_filestore(instrument, timeframe, quiet, False, with_index,convert_date_index_to_dt,use_full=use_full,tlid_range=tlid_range)
      else:
          print("run_jgtfxcli_on_error is OFF, not running jgtfxcli")
    except Exception as e:
        print("Error when running jgtfxcli")
        print(e)
        print("------------------------------------")
  
  
  if not quiet:
    print(df.columns)
    print(df.index)
    print("------------------------------------")

  if use_cache_full:
    add_df_to_full_cache(instrument, timeframe, df)
  return df


from datetime import datetime, timedelta
from pytz import timezone

def _get_dt_requirement_for_tf(timeframe,is_UTC=False): #@STCIssue The rest of the process might change the timezone from ours, not sure
  
  dt_now = str(datetime.now())
    
  return dt_now

def _if_crop_ph(dt_crop_last, df):
  if dt_crop_last is not None:
    return df[df.index <= dt_crop_last].copy() 
  return df


from datetime import datetime, timedelta
from pytz import timezone
def _get_dt_requirement_for_tf(timeframe, is_UTC=True):
  dt_now = datetime.now(timezone('EST')) if is_UTC else datetime.now()
  dt_friday_close = dt_now.replace(hour=16, minute=55, second=0, microsecond=0)

  # If it's the weekend, return the closing time of the previous Friday
  if dt_now.weekday() >= 5: 
    return dt_friday_close

  # If it's a weekday but after closing time, return the closing time of that day
  if dt_now.time() > dt_friday_close.time():
    return dt_friday_close

  # If it's a weekday and before closing time, return the closing time based on the timeframe
  closing_times = {
    'M1': dt_now.replace(hour=20, minute=44),
    'W1': dt_now.replace(hour=21),
    'D1': dt_now.replace(hour=21),
    'H8': dt_now.replace(hour=13),
    'H6': dt_now.replace(hour=15),
    'H4': dt_now.replace(hour=17),
    'H3': dt_now.replace(hour=18),
    'H2': dt_now.replace(hour=19),
    'H1': dt_now.replace(hour=20),
    'm30': dt_now.replace(hour=20, minute=30),
    'm15': dt_now.replace(hour=20, minute=45),
    'm5': dt_now.replace(hour=20, minute=40),
    'm1': dt_now.replace(hour=20, minute=44)
  }

  return closing_times.get(timeframe, dt_friday_close)


from dateutil.relativedelta import relativedelta

#@STCIssue NOT WORKING, Has a more complex logic.  ex.  H4 is not -4 but last bar completed less than 4 hours ago which fits in what the markets define as H4 (ex.  H4 is updated as 1:00, 5:00, 9:00, 13:00, 17:00, 21:00)
def get_dt_required_by_timeframes(input_datetime):
  # Convert the input string to a datetime object if not already
  if not isinstance(input_datetime, datetime):  input_datetime = datetime.strptime(input_datetime, "%Y-%m-%d %H:%M:%S")
  timeframes = {
    "M1": input_datetime - relativedelta(months=1),
    "W1": input_datetime - relativedelta(weeks=1),
    "D1": input_datetime - relativedelta(days=1),
    "H8": input_datetime.replace(hour=8, minute=0, second=0),
    "H6": input_datetime.replace(hour=6, minute=0, second=0),
    "H4": input_datetime.replace(hour=4, minute=0, second=0),
    "H3": input_datetime.replace(hour=3, minute=0, second=0),
    "H2": input_datetime.replace(hour=2, minute=0, second=0),
    "H1": input_datetime.replace(hour=1, minute=0, second=0),
    "m30": input_datetime.replace(minute=30, second=0),
    "m15": input_datetime.replace(minute=15, second=0),
    "m5": input_datetime.replace(minute=5, second=0),
    "m1": input_datetime.replace(minute=1, second=0)
  }
  return {k: v.strftime("%Y-%m-%d %H:%M:%S") for k, v in timeframes.items()}


def _test_if_having_crop_last_dt(df,crop_last_dt, quiet:bool=True):
    tst=df.tail(1).copy()
    if not quiet:
      print(" test_if_having_crop_last_dt")
      print("   crop_last_dt: " + str(crop_last_dt))
      print("   Last row: " + str(tst))
    tst = tst[tst.index >= crop_last_dt]
    return len(tst)>0 # Expecting 1 if we have the date


def _check_if_dt_range_has_enough_bars(instrument:str, timeframe:str, dt_last_we_want, quote_count_we_require:int, quiet:bool=True, use_full:bool=True):
    if not quiet:
      print("Checking if last row of full match out dt_crop_last with enough bars")
      print(" quote_count: " + str(quote_count_we_require) + " (REQUIRES enough bars after crops)")
      print(" dt_last_we_want: " + str(dt_last_we_want))
    try:
      df_full = getPH_from_filestore(instrument, timeframe, quiet=quiet, use_full=use_full)
      res= _test_if_having_crop_last_dt(df_full,dt_last_we_want) and len(df_full) >= quote_count_we_require
      if not quiet:
        if res:
          print("  Last row of full match out dt_crop_last with enough bars")
        else:
          print("  Last row of full does not match out dt_crop_last with enough bars")
      return res
    except Exception as e:
      #print(str(e))
      #print("Error in _check_if_dt_range_has_enough_bars")
      if not quiet:
        print("  Fixing issue with data....")
      return False


def if_select_start_end(df, start=None, end=None,quiet=True):
  if start is not None:
        
    if end is None:  # end is not provided
      end = datetime.now()
      
    if not quiet:
        print("start: " + str(start))
        print("end: " + str(end))
        
    if 'Date' in df.columns:
      mask = (df['Date'] >= start) & (df['Date'] <= end)
    else:
      mask = (df.index >= start) & (df.index <= end)
    
    selected_df = df.loc[mask].copy()
    return selected_df
  
  return df


def str_to_datetime(date_str):
    formats = ['%m.%d.%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%Y/%m/%d', '%Y-%m-%d']
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def getPH_from_filestore(instrument:str,timeframe:str,quiet=True, compressed:bool=False,with_index:bool=True,convert_date_index_to_dt:bool=True,
        tlid_range:str=None,
                         output_path=None,
                         nsdir:str="pds",
                         use_full:bool=False):
  """
  Retrieves OHLC data for a given instrument and timeframe from the filestore.

  Args:
    instrument (str): The instrument symbol.
    timeframe (str): The timeframe of the OHLC data.
    quiet (bool, optional): Whether to suppress print statements. Defaults to True.
    compressed (bool, optional): Whether the data is compressed. Defaults to False.
    with_index (bool, optional): Whether to include the index in the returned DataFrame. Defaults to True.
    convert_date_index_to_dt  (bool, optional): convert index Date to dt
    tlid_range (str, optional): Select a range on disk or return None if unavailable
    output_path (str, optional): The path to the output directory. Defaults to None.
    nsdir (str, optional): The name of the directory to use for the filestore. Defaults to "pds".
    use_full (bool, optional): Whether to read the full data. Defaults to False.

  Returns:
    pandas.DataFrame: The OHLC data for the given instrument and timeframe.
  """  
  
  srcpath = create_filestore_path(instrument, timeframe,quiet, compressed,tlid_range=tlid_range,output_path=output_path,nsdir=nsdir,use_full=use_full)
  
  print_quiet(quiet,srcpath)
  
  df = None
  try:
    df = read_ohlc_df_from_file(srcpath,quiet,compressed,with_index,convert_date_index_to_dt)
  except:
    pass 
  return df




def read_ohlc_df_from_file(srcpath, quiet=True, compressed=False,with_index=True,convert_date_index_to_dt=True):
  """
  Reads an OHLC (Open-High-Low-Close) +Date as DataFrame index from a CSV file.

  Args:
    srcpath (str): The path to the CSV file.
    quiet (bool, optional): Whether to print progress messages. Defaults to True.
    compressed (bool, optional): Whether the CSV file is compressed. Defaults to False.

  Returns:
    pandas.DataFrame: The OHLC DataFrame.
  """
  df = None
  try:
    if compressed:
      print_quiet(quiet, "Reading compressed: " + srcpath + " ")
      df = pd.read_csv(srcpath, compression=local_fn_compression)
    else:
      print_quiet(quiet, "Reading uncompressed csv file: " + srcpath)
      df = pd.read_csv(srcpath)
  except Exception as e:
    print_quiet(quiet,f"An error occurred while reading the file: {e}")
    df = None
  if with_index and df is not None:
    if 'Date' in df.columns:
      df.set_index('Date', inplace=True)
      
      if convert_date_index_to_dt:
        df.index = pd.to_datetime(df.index)
    else:
      raise ValueError("Column 'Date' is not present in the DataFrame")
  return df
 


def get_data_path():
    return jgtos.get_data_path('pds')
  
 

def get_pov_local_data_filename(instrument:str,timeframe:str,use_full=False):
  nsdir="pds"
  return jos.get_pov_local_data_filename(instrument,timeframe,use_full=use_full,nsdir=nsdir)


 

def get_instrument_properties(instrument:str, quiet=False,from_file=True):
  if not from_file:
    print("NOT SUPORTED in PDSP")
  else:
    
    # # Define the path to the directory
    instrument_properties = {}
    try:
      instrument_properties = iprops.get_iprop(instrument)
      instrument_properties["pipsize"] = instrument_properties["pips"]
    except:
      home_dir = os.path.expanduser("~")
      dir_path = os.path.join(home_dir, '.jgt', 'iprops')
      instrument_filename = instrument.replace("/", "-")
      #     # Read the instrument properties from the file
      iprop_dir_path = os.path.join(dir_path, f'{instrument_filename}.json')
      with open(iprop_dir_path, 'r') as f:
        instrument_properties = json.load(f)
    return instrument_properties


def print_quiet(quiet,content):
    if not quiet:
        print(content)
        
