debugging=False

import datetime as dt
import pandas as pd
import os
from . import JGTPDHelper as jpd
from . import jgtfxc as jfx
from .JGTConfig import local_fn_compression,get_pov_local_data_filename
from .JGTPDHelper import *
from .jgtfxc import *
# from .JGTConfig import *

# import .JGTPDHelper as jpd

# #import jgtpy.JGTFXCMWrapper as jfx
# import .jgtfxc as jfx



renameColumns=True
addOhlc=True
stayConnected=False

def stayConnectedSetter(_v,json_config_str=None):
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

def connect(quiet=True,json_config_str=None):  
  return jfx.connect(quiet,json_config_str)

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
  srcpath=get_pov_local_data_filename(instrument,timeframe)
  df=pd.read_csv(srcpath,compression=local_fn_compression,index_col='Date')
  return df


def get_data_path():
    data_path = os.environ.get('JGTPY_DATA', './data')

    if not os.path.exists(data_path):
      data_path = os.environ.get('JGTPY_DATA', '../data')
      

    if not os.path.exists(data_path):
      raise Exception("Data directory not found. Please create a directory named 'data' in the current or parent directory, or set the JGTPY_DATA environment variable.")
    
    data_path = os.path.join(data_path, 'pds')
    return data_path
  
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
  #print(df)
  # Define the file path based on the environment variable or local path
  fpath = write_df_to_filestore(df, instrument, timeframe, compressed)
  return fpath

def write_df_to_filestore(df, instrument, timeframe, compressed=False, quiet=True):
  
  fpath =  create_filestore_path(instrument, timeframe,quiet, compressed)
  
  if compressed:
    df.to_csv(fpath, compression=local_fn_compression)
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

    try:
        p=jfx.get_price_history(instrument, timeframe, start,end, quote_count+89,quiet=quiet)
    except:
        try:
            disconnect()
            connect(quiet=quiet)
            p=jfx.get_price_history(instrument, timeframe, start,end, quote_count+89,quiet=quiet)
        except:
            print("bahhhhhhhhhhhhhhhhhhhhhhh  REINITIALIZATION of the PDS todo")
            return


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
    
    #@STCIssue When we read from filestore, the Date Columnt is ok
    df =getPH_from_filestore(instrument,timeframe) #@STCIssue add start and end and index name should be already set
    if with_index:
      df.index.rename('Date',inplace=True)
      
    if start != None:
      mask = (df['Date'] > end) & (df['Date'] <= start)
      df = df.loc[mask]

  if addOhlc and renameColumns:
    df=pds_add_ohlc_stc_columns(df)
  if cleanseOriginalColumns:
    df=_cleanse_original_columns(df,debugging)
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



def get_instrument_properties(instrument, quiet=False):
  return jfx.get_instrument_properties(instrument, quiet)
    # # Define the path to the directory
    # home_dir = os.path.expanduser("~")
    # dir_path = os.path.join(home_dir, '.jgt', 'iprops')
    # instrument_properties = {}
    # instrument_filename = instrument.replace('/', '-')
    
    # # Check if the directory exists
    # if not os.path.exists(dir_path):
    #     # If not, create it
    #     os.makedirs(dir_path)
    
    # iprop_dir_path = os.path.join(dir_path, f'{instrument_filename}.json')
    # # Check if the file exists
    # if not os.path.exists(iprop_dir_path):
    #     # If not, create the directory if it doesn't exist
    #     if not os.path.exists(dir_path):
    #         os.makedirs(dir_path)

    #     # Define the instrument properties
    #     # Replace with your actual instrument properties
    #     pipsize = get_pipsize(instrument)
    #     instrument_properties = {
    #         "pipsize": pipsize
    #         # Add more properties as needed
    #     }

    #     # Replace forward slash with hyphen in the instrument name

    #     # Save the instrument properties to the file
    #     with open(iprop_dir_path, 'w') as f:
    #         json.dump(instrument_properties, f)

    #     if not quiet:
    #         print(f"Instrument properties for {instrument} saved.")
    # else:
    #     # Read the instrument properties from the file
    #     with open(iprop_dir_path, 'r') as f:
    #         instrument_properties = json.load(f)

    #     if not quiet:
    #         print(f"Instrument properties for {instrument} read.")
    # return instrument_properties


# Might move to JGTTDS later
def get_price_plus_minus_ticks(instrument, ticks_multiplier, context_price, direction_side):
  """
  Gets the price value plus or minus a defined number of ticks.

  Args:
  instrument: The instrument to trade.
  ticks_multiplier: The number of ticks to add or subtract.
  context_price: The current price of the instrument.
  direction_side: The direction side to use ('S' for minus, 'B' for plus).

  Returns:
  The price value plus or minus the defined number of ticks.
  """
  instrument_properties = get_instrument_properties(instrument)
  tick_size = instrument_properties.pipsize * ticks_multiplier
  if direction_side == 'S':
    price_minus_ticks = context_price - (ticks_multiplier * tick_size)
    return price_minus_ticks
  elif direction_side == 'B':
    price_plus_ticks = context_price + (ticks_multiplier * tick_size)
    return price_plus_ticks
  else:
    raise ValueError("Invalid direction side. Must be 'S' or 'B'.")


