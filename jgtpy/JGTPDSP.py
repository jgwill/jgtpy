
import datetime as dt
import pandas as pd
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import JGTPDHelper as jpd

from JGTConfig import local_fn_compression,get_pov_local_data_filename
from JGTPDHelper import *
from datetime import datetime
from jgtutils import jgtcommon,iprops,jgtos
from jgtutils.jgtos import create_filestore_path, mk_fn, mk_fn_range, mk_fullpath

from JGTChartConfig import JGTChartConfig

renameColumns=True
addOhlc=True


cleanseOriginalColumns=True
useLocal=True

def refreshPH(instrument:str, timeframe:str,quote_count:int=-1, quiet:bool=True,use_full:bool=False,verbose_level=0,tlid_range=None):
  from jgtutils import jgtwslhelper as wsl
  if not quiet:
    print(f"Refreshing {instrument} {timeframe}")
  try:
    wsl.getPH(instrument, timeframe,quote_count=quote_count, tlid_range=tlid_range, use_full=use_full,verbose_level=verbose_level)
  except Exception as e:
    print("Error in refreshPH")
    raise e

#df = df[df.index <= crop_last_dt]

def getPH_crop(instrument:str,
               timeframe:str,
               dt_crop_last,
               quote_count:int=-1,
               quiet:bool=True               
          ):
  if not quiet:  
    print("getting cropped data....")
    print(" dt_crop_last: " + str(dt_crop_last))
    print(" quote_count: " + str(quote_count))
  
  df=getPH(instrument, timeframe, quiet=quiet,dt_crop_last=dt_crop_last,use_full=True)
  
  ldf = len(df)
  #@q How can we Get Fresh data if the FULL has not our range ??
  
  if  ldf > quote_count  and quote_count != -1:
    if not quiet:
      print("  we selected: " + str(quote_count) + " bars")
    selected = df.iloc[-quote_count:].copy()
  else:
    selected = df.copy()
  return selected
  

def test_if_having_crop_last_dt(df,crop_last_dt, quiet:bool=True):
    tst=df.tail(1).copy()
    if not quiet:
      print(" test_if_having_crop_last_dt")
      print("   crop_last_dt: " + str(crop_last_dt))
      print("   Last row: " + str(tst))
    tst = tst[tst.index >= crop_last_dt]
    return len(tst)>0 # Expecting 1 if we have the date


def _check_if_last_row_of_full_match_out_dt_crop_last_with_enough_bars(instrument:str, timeframe:str, dt_crop_last, quote_count:int, quiet:bool=True):
      if not quiet:
        print("Checking if last row of full match out dt_crop_last with enough bars")
        print(" quote_count: " + str(quote_count) + " (REQUIRES enough bars after crops)")
      df_full = getPH_from_filestore(instrument, timeframe, quiet=quiet, use_full=True)
      res= test_if_having_crop_last_dt(df_full,dt_crop_last) and len(df_full) >= quote_count
      if not quiet:
        if res:
          print("  Last row of full match out dt_crop_last with enough bars")
        else:
          print("  Last row of full does not match out dt_crop_last with enough bars")
      return res


def getPH(instrument:str, timeframe:str, quote_count:int=-1, start=None, end=None, with_index=True, quiet:bool=True,convert_date_index_to_dt:bool=True,cc: JGTChartConfig=None,get_them_all:bool=False,use_full:bool=False,
          dt_crop_last=None,
          tlid_range=None,
    run_jgtfxcli_on_error=True,
    use_fresh=False,
    use_fresh_error_ignore=False
          ):
  #@STCissue quote_count is ignored or irrelevant in start/end
  #@a Adequate start and end from the stored file
  if cc is None:
    cc = JGTChartConfig()
  if quote_count == -1 and use_full == False: #@STCIssue JGTChartConfig being Replaced by JGTPDSPRequest
    quote_count = cc.nb_bar_to_retrieve
  
  # If we dont have enough data in full when using crop_last_dt, we should use fresh
  if dt_crop_last is not None and use_full:
    our_data_is_ok=_check_if_last_row_of_full_match_out_dt_crop_last_with_enough_bars(instrument, timeframe, dt_crop_last, quote_count, quiet)
    if not our_data_is_ok:
      if not quiet:
        print("Our data is not ok, using fresh")
      use_fresh=True
    else:
      if not quiet:
        print("Our data is ok, not using fresh")
    
    
  
  if use_fresh:
    try:
      refreshPH(instrument, timeframe,quote_count=quote_count, tlid_range=tlid_range, use_full=use_full,verbose_level=1)
    except: #Raise ExceptionUseFreshData
      print("Error in getPH, use_fresh failed")
      if use_fresh_error_ignore:
        pass      
      raise Exception("Error in getPH, use_fresh failed")
    
  df = getPH_from_filestore(instrument, timeframe, quiet, False, with_index,convert_date_index_to_dt,use_full=use_full,tlid_range=tlid_range)
  if df  is None and run_jgtfxcli_on_error:
    print("NO DATA IN DF, running jgtfxcli")
    #df = getPH_from_filestore(instrument, timeframe, quiet, False, with_index,convert_date_index_to_dt,use_full=use_full)
    #@STCIssue its more PDSP that should run this logics
    try: 
      if run_jgtfxcli_on_error:
        print("Error in createFromPDSFile, running jgtfxcli")
        refreshPH(instrument, timeframe,quote_count=quote_count, tlid_range=tlid_range, use_full=use_full,verbose_level=1)
        # CALL IT BACK AGAIN
        df = getPH_from_filestore(instrument, timeframe, quiet, False, with_index,convert_date_index_to_dt,use_full=use_full,tlid_range=tlid_range)
      else:
          print("run_jgtfxcli_on_error is OFF, not running jgtfxcli")
    except Exception as e:
        print("Error in createFromPDSFile, jgtfxcli failed")
        print(e)
    
    
  if not quiet:
    print(df.columns)
    print(df.index)
    print("------------------------------------")
  
  if start is not None:
    #@STCIssue Not supported supplying the 'end' with a count
    if end is None:  # end is not provided
      end = datetime.now()
    
    if not quiet:
      print("start: " + str(start))
      print("end: " + str(end))
    df = select_start_end(df, start, end)
    
  if dt_crop_last is not None:
    df = df[df.index <= dt_crop_last]
      
  ldf = len(df)
  if ldf > quote_count and not get_them_all and quote_count > 50:
    if not use_full:
      df = df.iloc[-quote_count:]
  
  return df

def select_start_end(df, start, end=None):
  if end is None:  # end is not provided
    end = datetime.now()
  
  if 'Date' in df.columns:
    mask = (df['Date'] >= start) & (df['Date'] <= end)
  else:
    mask = (df.index >= start) & (df.index <= end)
  
  selected_df = df.loc[mask]
  return selected_df


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
    print(f"An error occurred while reading the file: {e}")
    df = None
  if with_index:
    if 'Date' in df.columns:
      df.set_index('Date', inplace=True)
      
      if convert_date_index_to_dt:
        df.index = pd.to_datetime(df.index)
    else:
      raise ValueError("Column 'Date' is not present in the DataFrame")
  return df
 


def get_data_path():
    return jgtos.get_data_path('pds')
  
  

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
        
