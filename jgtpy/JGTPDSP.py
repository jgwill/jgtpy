
import datetime as dt
import pandas as pd
import os
from . import JGTPDHelper as jpd


from .JGTConfig import local_fn_compression,get_pov_local_data_filename
from .JGTPDHelper import *



renameColumns=True
addOhlc=True


cleanseOriginalColumns=True
useLocal=True

def getPH_from_filestore(instrument,timeframe,quiet=True, compressed=False,with_index=True):
  """
  Retrieves OHLC data for a given instrument and timeframe from the filestore.

  Args:
    instrument (str): The instrument symbol.
    timeframe (str): The timeframe of the OHLC data.
    quiet (bool, optional): Whether to suppress print statements. Defaults to True.
    compressed (bool, optional): Whether the data is compressed. Defaults to False.
    with_index (bool, optional): Whether to include the index in the returned DataFrame. Defaults to True.

  Returns:
    pandas.DataFrame: The OHLC data for the given instrument and timeframe.
  """  
  srcpath = create_filestore_path(instrument, timeframe,quiet, compressed)  
  
  print_quiet(quiet,srcpath)
  
  df = read_ohlc_df_from_file(srcpath,quiet,compressed,with_index)
  
  return df




def read_ohlc_df_from_file(srcpath, quiet=True, compressed=False,with_index=True):
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
  #path + '/'+fn
  return rpath
#.replace('..','.').replace('//','/')





def get_data_path():
    data_path = os.environ.get('JGTPY_DATA', './data')

    if not os.path.exists(data_path):
      data_path = os.environ.get('JGTPY_DATA', '../data')
      

    if not os.path.exists(data_path):
      raise Exception("Data directory not found. Please create a directory named 'data' in the current or parent directory, or set the JGTPY_DATA environment variable.")
    
    data_path = os.path.join(data_path, 'pds')
    return data_path
  
  
  


def print_quiet(quiet,content):
    if not quiet:
        print(content)
        