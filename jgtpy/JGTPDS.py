import datetime as dt
import pandas as pd
import os

from . import JGTPDHelper as jpd

#import jgtpy.JGTFXCMWrapper as jfx
from . import jgtfxc as jfx

from . import JGTConfig as jgtcnf


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


def mk_fn(_instrument,_timeframe,_ext):
  """Make a file name with instrument and timeframe

  Args:
      _instrument (str): symbol
      _timeframe (str): TF
      _ext (str): ext name "csv"

  Returns:
      str: file name
  """
  _tf = _timeframe
  _i= _instrument.replace('/','-')
  if _timeframe == 'm1':
    _tf = _timeframe.replace('m1','mi1')
  _fn= _i + '_' + _tf + '.' + _ext
  return _fn.replace('..','.')

def mk_fullpath(_instrument,_timeframe,_ext,_path):
  _fn=mk_fn(_instrument,_timeframe,_ext)
  _r= _path + '/'+_fn
  return _r.replace('..','.').replace('//','/')





def pds_add_ohlc_stc_columns(dfsrc):
  if not 'Open' in dfsrc.columns:
    dfsrc['Open'] = dfsrc[['BidOpen', 'AskOpen']].mean(axis=1)
    dfsrc['High'] = dfsrc[['BidHigh', 'AskHigh']].mean(axis=1)
    dfsrc['Low'] = dfsrc[['BidLow', 'AskLow']].mean(axis=1)
    dfsrc['Close'] = dfsrc[['BidClose', 'AskClose']].mean(axis=1)
    #Median
    dfsrc['Median']= ((dfsrc['High'] + dfsrc['Low']) / 2)
    return dfsrc


def __cleanse_original_columns(dfsrc,_quiet=True):
  dfsrc=jpd.pds_cleanse_original_columns(dfsrc,_quiet)
  return dfsrc


def getSubscribed():
  return jfx.con.get_instruments_for_candles()

def connect(quiet=True):  
  return jfx.connect(quiet)

def disconnect(quiet=True):
  return jfx.disconnect(quiet)

def tryConnect():
  try:
    con=connect()
  except ConnectionError:
    print("Connection error")

def status():
  return jfx.status()

def getPH_from_local1(instrument,timeframe):
  srcpath=jgtcnf.get_pov_local_data_filename(instrument,timeframe)
  df=pd.read_csv(srcpath,compression=jgtcnf.local_fn_compression,index_col='Date')
  return df

def getPH_from_local(instrument,timeframe,quiet=True):
  # Define the file path based on the environment variable or local path
  data_path = os.environ.get('JGTPY_DATA', './data')
  fn=mk_fn(instrument,timeframe,'csv')
  srcpath=mk_fullpath(instrument,timeframe,'csv',data_path)
  if not quiet  :
    print(srcpath)
  # df=pd.read_csv(srcpath,index_col='Date')
  df=pd.read_csv(srcpath)
  return df

def getPH_to_file(instrument,timeframe,quote_count=335,start=None,end=None,with_index=True,quiet=True,compressed=False):
  # Define the file path based on the environment variable or local path
  data_path = os.environ.get('JGTPY_DATA', './data')
  fpath=mk_fullpath(instrument,timeframe,'csv',data_path)
  df=getPH(instrument,timeframe,quote_count,start,end,False,quiet)
  if compressed:
    df.to_csv(fpath,compression=jgtcnf.local_fn_compression)
  else:
    df.to_csv(fpath)
  return fpath

def getPH2file(instrument,timeframe,quote_count=335,start=None,end=None,with_index=True,quiet=True,compressed=False):
  return getPH_to_file(instrument,timeframe,quote_count,start,end,with_index,quiet,compressed)

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
    #print("------------DATAFRAME----------------")
    #print(df)

    #mask = (df['Date'] > start) & (df['Date'] <= end)
    #df = df.loc[mask]

    if not stayConnected:
      con=disconnect(quiet=quiet)
    if renameColumns:
      df=df.rename(columns={'bidopen': 'BidOpen', 'bidhigh': 'BidHigh','bidclose':'BidClose','bidlow':'BidLow','askopen': 'AskOpen', 'askhigh': 'AskHigh','askclose':'AskClose','asklow':'AskLow','tickqty':'Volume','date':'Date'})
      df= df.astype({'Volume':int})
    if with_index:
      df.index.rename('Date',inplace=True)
  else:
    #Read from local
    df =getPH_from_local(instrument,timeframe)
    if with_index:
      df.index.rename('Date',inplace=True)
    if start != None:
      mask = (df['Date'] > end) & (df['Date'] <= start)
      df = df.loc[mask]
  
  # df=df.rename_axis(index=None, columns=None)
  # df.index.rename('Date', inplace=True)
  if addOhlc and renameColumns:
    df=pds_add_ohlc_stc_columns(df)
  if cleanseOriginalColumns:
    df=__cleanse_original_columns(df)
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
    df=jfx.con.get_candles(instrument, period=timeframe,with_index=with_index,start=start,end=end)
    if not stayConnected:
      con=disconnect(quiet=quiet)
    if renameColumns:
      df=df.rename(columns={'bidopen': 'BidOpen', 'bidhigh': 'BidHigh','bidclose':'BidClose','bidlow':'BidLow','askopen': 'AskOpen', 'askhigh': 'AskHigh','askclose':'AskClose','asklow':'AskLow','tickqty':'Volume','date':'Date'})
      df= df.astype({'Volume':int})
      if with_index:
        df.index.rename('Date',inplace=True)
  else:
    #Read from local
    df =getPH_from_local(instrument,timeframe) 
    if with_index:
        df.index.rename('Date',inplace=True)
    mask = (df['Date'] > end) & (df['Date'] <= start)
    df = df.loc[mask]
  #print(df)
  #df.to_csv("data.csv")
  #mask = (df['Date'] > end) & (df['Date'] <= start)
  #df = df.loc[mask]
  # df=df.rename_axis(index=None, columns=None)
  # df.index.rename('Date', inplace=True)
  if addOhlc and renameColumns:
    df=pds_add_ohlc_stc_columns(df)
  if cleanseOriginalColumns:
    df=__cleanse_original_columns(df)
  return df



def getPresentBarAsList(_df):
  _paf =_df.iloc[-1:]
  _pa = _paf.to_dict(orient='list')
  _dtctx=str(_paf.index.values[0])
  _pa['Date'] = _dtctx
  return _pa

def getLastCompletedBarAsList(_df):
  _paf =_df.iloc[-2:-1]
  _pa = _paf.to_dict(orient='list')
  _dtctx=str(_paf.index.values[0])
  _pa['Date'] = _dtctx
  return _pa

  
