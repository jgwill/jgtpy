
import datetime as dt
import pandas as pd
import os
import json
from . import JGTPDHelper as jpd

from .JGTConfig import local_fn_compression,get_pov_local_data_filename
from .JGTPDHelper import *
from datetime import datetime



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


def getPH_from_filestore(instrument,timeframe,quiet=True, compressed=False,with_index=True,convert_date_index_to_dt=True):
  """
  Retrieves OHLC data for a given instrument and timeframe from the filestore.

  Args:
    instrument (str): The instrument symbol.
    timeframe (str): The timeframe of the OHLC data.
    quiet (bool, optional): Whether to suppress print statements. Defaults to True.
    compressed (bool, optional): Whether the data is compressed. Defaults to False.
    with_index (bool, optional): Whether to include the index in the returned DataFrame. Defaults to True.
    convert_date_index_to_dt  (bool, optional): convert index Date to dt

  Returns:
    pandas.DataFrame: The OHLC data for the given instrument and timeframe.
  """  
  srcpath = create_filestore_path(instrument, timeframe,quiet, compressed)  
  
  print_quiet(quiet,srcpath)
  
  df = read_ohlc_df_from_file(srcpath,quiet,compressed,with_index,convert_date_index_to_dt)

  
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



def create_filestore_path(instrument, timeframe,quiet=True, compressed=False):
    # Define the file path based on the environment variable or local path
    data_path = get_data_path()
    print(data_path)

    ext = 'csv'
    if compressed:
        ext = 'csv.gz'
    fpath = mk_fullpath(instrument, timeframe, ext, data_path)
    if os.name == 'nt':
      fpath = fpath.replace('/', '\\')
    return fpath
  
  
def mk_fn(instrument,timeframe,ext):
  """Make a file name with instrument and timeframe

  Args:
      _instrument (str): symbol
      _timeframe (str): TF
      _ext (str): ext name "csv"

  Returns:
      str: file name
  """
  _tf = timeframe
  _i= instrument.replace('/','-')
  if timeframe == 'm1':
    _tf = timeframe.replace('m1','mi1')
  _fn= _i + '_' + _tf + '.' + ext
  return _fn.replace('..','.')


def mk_fullpath(instrument,timeframe,ext,path):
  fn=mk_fn(instrument,timeframe,ext)
  rpath= os.path.join(path,fn)
  if os.name == 'nt':
    rpath= rpath.replace('/', '\\')
  #path + '/'+fn
  return rpath
#.replace('..','.').replace('//','/')





def get_data_path():
    default_dot = './data'
    default_dotdot = '../data'
    data_path = os.environ.get('JGTPY_DATA', default_dot)

    if not os.path.exists(data_path):
      data_path = os.environ.get('JGTPY_DATA', default_dotdot)
      
    if os.name == 'nt':
      data_path = data_path.replace('/', '\\')

    if not os.path.exists(data_path):
      raise Exception("Data directory not found. Please create a directory named 'data' in the current or parent directory, or set the JGTPY_DATA environment variable.")
    
    data_path = os.path.join(data_path, 'pds')
    return data_path
  
  


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
        