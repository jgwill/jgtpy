import datetime as dt
import pandas as pd
import os
from . import JGTPDHelper as jpd
from . import jgtfxc as jfx
from . import JGTConfig as jgtcnf
from .JGTPDHelper import *
from .jgtfxc import *
from .JGTConfig import *

# import .JGTPDHelper as jpd

# #import jgtpy.JGTFXCMWrapper as jfx
# import .jgtfxc as jfx

# import .JGTConfig as jgtcnf


renameColumns=True
addOhlc=True
stayConnected=False

def stayConnectedSetter(_v):
  global stayConnected
  stayConnected=_v
  jfx.stayConnected=_v
  jfx.connect()
  
cleanseOriginalColumns=True
useLocal=False
con=None


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





def pds_add_ohlc_stc_columns(dfsrc):
  if not 'Open' in dfsrc.columns:
    dfsrc['Open'] = dfsrc[['BidOpen', 'AskOpen']].mean(axis=1)
    dfsrc['High'] = dfsrc[['BidHigh', 'AskHigh']].mean(axis=1)
    dfsrc['Low'] = dfsrc[['BidLow', 'AskLow']].mean(axis=1)
    dfsrc['Close'] = dfsrc[['BidClose', 'AskClose']].mean(axis=1)
    #Median
    dfsrc['Median']= ((dfsrc['High'] + dfsrc['Low']) / 2)
    return dfsrc


def _cleanse_original_columns(dfsrc,quiet=True):
  dfsrc=jpd.pds_cleanse_original_columns(dfsrc,quiet)
  return dfsrc


def getSubscribed():
  print("REQUIRE UPGRADE FOR THIS FUNCTION (fxcmpy DEPRECRATED)")
  print("--------------------------------------")
  return "REQUIRE UPGRADE FOR THIS FUNCTION (fxcmpy DEPRECRATED)"
  #return jfx.con.get_instruments_for_candles()

def connect(quiet=True):  
  return jfx.connect(quiet)

def disconnect(quiet=True):
  return jfx.disconnect(quiet)

def tryConnect():
  try:
    con=connect()
  except ConnectionError:
    print("Connection error")

def status(quiet=True):
  return jfx.status(quiet)

def getPH_from_local1(instrument,timeframe):
  srcpath=jgtcnf.get_pov_local_data_filename(instrument,timeframe)
  df=pd.read_csv(srcpath,compression=jgtcnf.local_fn_compression,index_col='Date')
  return df


def get_data_path():
    data_path = os.environ.get('JGTPY_DATA', './data')

    if not os.path.exists(data_path):
      data_path = os.environ.get('JGTPY_DATA', '../data')
      

    if not os.path.exists(data_path):
      raise Exception("Data directory not found. Please create a directory named 'data' in the current or parent directory, or set the JGTPY_DATA environment variable.")
    
    data_path = os.path.join(data_path, 'pds')
    return data_path
  
def getPH_from_filestore(instrument,timeframe,quiet=True, compressed=False):
  # Define the file path based on the environment variable or local path
  # data_path = get_data_path()
  # fn=mk_fn(instrument,timeframe,'csv')
  
  # srcpath=mk_fullpath(instrument,timeframe,'csv',data_path)
  srcpath = create_filestore_path(instrument, timeframe,quiet, compressed)  
  
  print_quiet(quiet,srcpath)
  
  df = read_ohlc_df_from_file(srcpath,quiet,compressed)
  
  return df

import pandas as pd


def read_ohlc_df_from_file(srcpath, quiet=True, compressed=False):
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
      df = pd.read_csv(srcpath, compression=jgtcnf.local_fn_compression)
    else:
      print_quiet(quiet, "Reading uncompressed csv file: " + srcpath)
      df = pd.read_csv(srcpath)
  except Exception as e:
    print(f"An error occurred while reading the file: {e}")
    df = None
    
  if 'Date' in df.columns:
    df.set_index('Date', inplace=True)
  else:
    raise ValueError("Column 'Date' is not present in the DataFrame")

  return df


def getPH_to_filestore(instrument, timeframe, quote_count=335, start=None, end=None, with_index=True, quiet=True, compressed=False):
  """
  Saves the OHLC data for a given instrument and timeframe to a CSV file.

  Args:
  - instrument (str): The instrument symbol (e.g. 'AAPL')
  - timeframe (str): The timeframe for the data (e.g. '1D' for daily, '1H' for hourly)
  - quote_count (int): The number of quotes to retrieve (default: 335)
  - start (str): The start date for the data (default: None)
  - end (str): The end date for the data (default: None)
  - with_index (bool): Whether to include the index in the CSV file (default: True)
  - quiet (bool): Whether to suppress console output (default: True)
  - compressed (bool): Whether to compress the CSV file using gzip (default: False)

  Returns:
  - str: The file path where the CSV file was saved.
  """
  df=getPH(instrument,timeframe,quote_count,start,end,False,quiet)
  
  # Define the file path based on the environment variable or local path
  fpath = write_df_to_filestore(df, instrument, timeframe, compressed)
  return fpath

def write_df_to_filestore(df, instrument, timeframe, compressed=False, quiet=True):
  
  fpath =  create_filestore_path(instrument, timeframe,quiet, compressed)
  
  if compressed:
    df.to_csv(fpath, compression=jgtcnf.local_fn_compression)
  else:
    df.to_csv(fpath)
  
  return fpath


def create_filestore_path(instrument, timeframe,quiet=True, compressed=False):
    # Define the file path based on the environment variable or local path
    data_path = get_data_path()
    ext = 'csv'
    if compressed:
        ext = 'csv.gz'
    fpath = mk_fullpath(instrument, timeframe, ext, data_path)
    return fpath
  
def getPH2file(instrument,timeframe,quote_count=335,start=None,end=None,with_index=True,quiet=True,compressed=False):
  return getPH_to_filestore(instrument,timeframe,quote_count,start,end,with_index,quiet,compressed)

def getPH(instrument,timeframe,quote_count=335,start=None,end=None,with_index=True,quiet=True):
  """Get Price History from Broker

  Args:
      instrument (str): symbal
      timeframe (str): TF
      quote_count (int, optional): nb bar to retrieve. Defaults to 335.
      start (str, optional): start DateTime. Defaults to None.
      end (str, optional): end DateTime range. Defaults to None.
      with_index (bool, optional): Return DataFrame with Index. Defaults to True.
      quiet  (bool, optional): stay calm ;)

  Returns:
      pandas.DataFrame: DF with price histories
  """
  df = pd.DataFrame()
  if not useLocal:
    con=connect(quiet=quiet)

    p=jfx.get_price_history(instrument, timeframe, start,end, quote_count+89)
    #print(p)
    df=pd.DataFrame(p,columns=['Date','BidOpen','BidHigh','BidLow','BidClose','AskOpen','AskHigh','AskLow','AskClose','Volume'])

    if not stayConnected:
      con=disconnect(quiet=quiet)
    if renameColumns:
      df=df.rename(columns={'bidopen': 'BidOpen', 'bidhigh': 'BidHigh','bidclose':'BidClose','bidlow':'BidLow','askopen': 'AskOpen', 'askhigh': 'AskHigh','askclose':'AskClose','asklow':'AskLow','tickqty':'Volume','date':'Date'})
      df= df.astype({'Volume':int})
    if with_index:
      df.index.rename('Date',inplace=True)
  else:
    #Read from local
    df =getPH_from_filestore(instrument,timeframe) #@STCIssue add start and end and index name should be already set
    if with_index:
      df.index.rename('Date',inplace=True)
    if start != None:
      mask = (df['Date'] > end) & (df['Date'] <= start)
      df = df.loc[mask]

  if addOhlc and renameColumns:
    df=pds_add_ohlc_stc_columns(df)
  if cleanseOriginalColumns:
    df=_cleanse_original_columns(df)
  # Set 'Date' column as the index
  df.set_index('Date', inplace=True)
  return df


def getPHByRange(instrument,timeframe,start=None,end=None,with_index=True,quiet=True):
  """Get Price History from Broker

  Args:
      instrument (str): symbal
      timeframe (str): TF
      start (str, optional): start DateTime. Defaults to None.
      end (str, optional): end DateTime range. Defaults to None.
      with_index (bool, optional): Return DataFrame with Index. Defaults to True.
      quiet  (bool, optional): stay calm ;)

  Returns:
      pandas.DataFrame: DF with price histories
  """
  df = pd.DataFrame()
  #if disconnected:
  # con=connect()
  if not useLocal:
    con=connect(quiet=quiet)
    df=getPH(instrument, timeframe,with_index=with_index,start=start,end=end,quiet=quiet)
    #print(df)
    
    # if addOhlc and renameColumns:
    #   df=pds_add_ohlc_stc_columns(df)
    # if cleanseOriginalColumns:
    #   df=_cleanse_original_columns(df)
    
    if not stayConnected:
       con=disconnect(quiet=quiet)

  else:
    #Read from local
    print_quiet(quiet,"Reading from local")
    df =getPH_from_filestore(instrument,timeframe) 
    

    
    if 'Date' in df.columns and start >= df['Date'].min() and end <= df['Date'].max():
        mask = (df['Date'] > end) & (df['Date'] <= start)
        df = df.loc[mask]
    else:
        raise PDSRangeNotAvailableException("The specified range is not available in the DataFrame")
 
  return df



def getPresentBarAsList(dfsrc):
  _paf =dfsrc.iloc[-1:]
  _pa = _paf.to_dict(orient='list')
  _dtctx=str(_paf.index.values[0])
  _pa['Date'] = _dtctx
  return _pa

def getLastCompletedBarAsList(dfsrc):
  _paf =dfsrc.iloc[-2:-1]
  _pa = _paf.to_dict(orient='list')
  _dtctx=str(_paf.index.values[0])
  _pa['Date'] = _dtctx
  return _pa

  


def print_quiet(quiet,content):
    if not quiet:
        print(content)
        
        
class PDSRangeNotAvailableException(Exception):
    pass
