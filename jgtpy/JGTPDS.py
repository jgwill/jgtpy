import datetime as dt
import pandas as pd
import jgtpy.JGTPDHelper as jpd

import jgtpy.JGTFXCMWrapper as jfx
import jgtpy.JGTConfig as jgtcnf



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





def pds_add_ohlc_stc_columns(_df):
  if not 'Open' in _df.columns:
    _df['Open'] = _df[['BidOpen', 'AskOpen']].mean(axis=1)
    _df['High'] = _df[['BidHigh', 'AskHigh']].mean(axis=1)
    _df['Low'] = _df[['BidLow', 'AskLow']].mean(axis=1)
    _df['Close'] = _df[['BidClose', 'AskClose']].mean(axis=1)
    #Median
    _df['Median']= ((_df['High'] + _df['Low']) / 2)
    return _df


def __cleanse_original_columns(_df,_quiet=True):
  _df=jpd.pds_cleanse_original_columns(_df,_quiet)
  return _df


def getSubscribed():
  return jfx.con.get_instruments_for_candles()

def connect(quiet=True):
  return jfx.connect(quiet)

def disconnect(quiet=True):
  return jfx.disconnect(quiet)

renameColumns=True
addOhlc=True
stayConnected=False
cleanseOriginalColumns=True
useLocal=False
con=None

def tryConnect():
  try:
    con=connect()
  except ConnectionError:
    print("Connection error")
    
def getPH_from_local(instrument,timeframe):
  srcpath=jgtcnf.get_pov_local_data_filename(instrument,timeframe)
  df=pd.read_csv(srcpath,compression=jgtcnf.local_fn_compression,index_col='Date')
  return df

def getPH(instrument,timeframe,number=335,start=None,end=None,with_index=True,quiet=True):
  """Get Price History from Broker

  Args:
      instrument (str): symbal
      timeframe (str): TF
      number (int, optional): nb bar to retrieve. Defaults to 335.
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
    if start == None:
      df=jfx.con.get_candles(instrument, period=timeframe, number=number+89,with_index=with_index)
    else:
      df=jfx.con.get_candles(instrument, period=timeframe,with_index=with_index,start=start,end=end)
      mask = (df['Date'] > start) & (df['Date'] <= end)
      df = df.loc[mask]
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

  
