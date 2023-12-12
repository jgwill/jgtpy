
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
import jgtcommon
import jgtos

renameColumns=True
addOhlc=True


cleanseOriginalColumns=True
useLocal=True


def getPH(instrument, timeframe, quote_count=335, start=None, end=None, with_index=True, quiet=True,convert_date_index_to_dt=True):
  #@STCissue quote_count is ignored or irrelevant in start/end
  #@a Adequate start and end from the stored file

  df = getPH_from_filestore(instrument, timeframe, quiet, False, with_index,convert_date_index_to_dt)
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


def getPH_from_filestore(instrument,timeframe,quiet=True, compressed=False,with_index=True,convert_date_index_to_dt=True,tlid_range=None):
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

  Returns:
    pandas.DataFrame: The OHLC data for the given instrument and timeframe.
  """  
  srcpath = create_filestore_path(instrument, timeframe,quiet, compressed,tlid_range=tlid_range)  
  
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



def create_filestore_path(instrument, timeframe,quiet=True, compressed=False,tlid_range=None,output_path=None):
  return jgtos.create_filestore_path(instrument,timeframe,quiet,compressed,tlid_range,output_path)
  
  
def mk_fn(instrument,timeframe,ext="csv"):
  return jgtos.mk_fn(instrument,timeframe,ext)


def mk_fn_range(instrument, timeframe, start: datetime, end: datetime,ext="csv"):
  return jgtos.mk_fn_range(instrument,timeframe,start,end,ext)


def mk_fullpath(instrument,timeframe,ext,path,tlid_range=None):
  return jgtos.mk_fullpath(instrument,timeframe,ext,path,tlid_range)


def get_data_path():
    return jgtos.get_data_path()
  
  


def get_instrument_properties(instrument, quiet=False,from_file=True):
  if not from_file:
    print("NOT SUPORTED in PDSP")
  else:
    
    # # Define the path to the directory
    home_dir = os.path.expanduser("~")
    dir_path = os.path.join(home_dir, '.jgt', 'iprops')
    instrument_properties = {}
    instrument_filename = instrument.replace('/', '-')
    #     # Read the instrument properties from the file
    iprop_dir_path = os.path.join(dir_path, f'{instrument_filename}.json')
    with open(iprop_dir_path, 'r') as f:
      instrument_properties = json.load(f)
    return instrument_properties


def print_quiet(quiet,content):
    if not quiet:
        print(content)
        