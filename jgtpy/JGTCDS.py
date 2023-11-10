# %%

from . import JGTPDS as pds
from . import JGTIDS as ids

import pandas as pd
import os

def startSession():
  pds.connect()
  
def stopSession():
  pds.dis
# %%

def createFromPDSFile(_instrument,_timeframe,quiet=True):
  """Create CDS (Chaos Data Service) with Fresh Data

  Args:
      _instrument (str): symbol
      _timeframe (str): TF
      _path (str): path to file

  Returns:
      pandas.DataFrame: CDS DataFrame
  """
  df=pds.getPH_from_local(_instrument,_timeframe)
  if not quiet:
    print(df)
  dfi=createFromDF(df)
  return dfi

def createFromDF(df, quiet=True):
  """
  Creates a new DataFrame with indicators, signals, and cleansed columns added based on the input DataFrame.

  Args:
    df (pandas.DataFrame): The input DataFrame to add indicators, signals, and cleansed columns to.
    quiet (bool, optional): Whether to suppress console output during processing. Defaults to True.

  Returns:
    pandas.DataFrame: The new DataFrame with indicators, signals, and cleansed columns added.
  """
  dfi=ids.ids_add_indicators(df,quiet=quiet)
  dfi=ids.cds_add_signals_to_indicators(dfi,quiet=quiet)
  dfi=ids.jgti_add_zlc_plus_other_AO_signal(dfi,quiet=quiet)
  dfi=ids.pds_cleanse_original_columns(dfi,quiet=quiet)
  dfi =ids.__ids_cleanse_ao_peak_secondary_columns(dfi,quiet=True)
  return dfi


def create(instrument,timeframe,nb2retrieve=335,stayConnected=False,quiet=True):
  """Create CDS (Chaos Data Service) with Fresh Data

  Args:
      instrument (str): symbol
      timeframe (str): TF
      nb2retrieve (int, optional): nb bar to retrieve. Defaults to 335.
      stayConnected (bool, optional): Leave Forexconnect connected. Defaults to False.
      quiet (bool,optional): Output quiet

  Returns:
      pandas.DataFrame: CDS DataFrame
  """
  pds.stayConnected=stayConnected
  df=pds.getPH(instrument,timeframe,nb2retrieve,with_index=False,quiet=quiet)
  dfi=createFromDF(df,quiet=quiet)
  return dfi
  

#createByRange
def createByRange(instrument,timeframe,start,end,stayConnected=False,quiet=True):
  """Create CDS with Fresh Data from a range

  Args:
      instrument (str): symbol
      timeframe (str): TF
      start (date): start date
      end (date): end date
      stayConnected (bool, optional): Leave FXCMPY connected. Defaults to False.
      quiet (bool,optional): Output quiet

  Returns:
      pandas.DataFrame: CDS DataFrame
  """
  pds.stayConnected=stayConnected
  df=pds.getPHByRange(instrument,timeframe,start,end,with_index=False,quiet=quiet)
  dfi=createFromDF(df,quiet=quiet)
  return dfi





columns_to_remove = ['aofvalue', 'aofhighao', 'aoflowao', 'aofhigh', 'aoflow', 'aocolor', 'accolor', 'fdbbhigh', 'fdbblow', 'fdbshigh', 'fdbslow']

def createFromFile_and_clean_and_save_data(instrument, timeframe):
    # Create DataFrame from PDS file
    c = createFromPDSFile(instrument, timeframe)

    # Remove specified columns if provided
    if columns_to_remove:
        c = c.drop(columns=columns_to_remove, errors='ignore')

    # Define the file path based on the environment variable or local path
    data_path = os.environ.get('JGTPY_DATA', './data')
    data_path = os.path.join(data_path, 'cds')
    fpath = pds.mk_fullpath(instrument, timeframe, 'csv', data_path)

    # Set 'Date' as the index
    c.set_index('Date', inplace=True)

    # Save DataFrame to CSV
    c.to_csv(fpath)

    return c









def getSubscribed():
  return pds.getSubscribed()

def getActiveSymbols():
  AppSuiteConfigRootPath = os.getenv('AppSuiteConfigRootPath')
  fn='activesymbol.txt'
  fpath=os.path.join(AppSuiteConfigRootPath,fn)
  with open(fpath) as f:
    first_line = f.readline()
    print(first_line)

# %%
def getLast(_df):
  return _df.iloc[-1]

def getPresentBar(_df):
  r= _df#['High','Low',indicator_AO_awesomeOscillator_column_name,signalCode_fractalDivergentBar_column_name,indicator_AC_accelerationDeceleration_column_name]
  return r.iloc[-1:]

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





def checkFDB(_instrument,_timeframe):
  _df=create(_instrument)
  pa = getPresentBarAsList(_df)
  isfdb = pa[signalCode_fractalDivergentBar_column_name][0]  != 0.0
  fdb = pa[signalCode_fractalDivergentBar_column_name]
  dtctx = pa['Date']
  if isfdb:
    print(_instrument + "_" + _timeframe + " : We Have a Signal : " + dtctx)
    return True
  else:
    print(_instrument + "_" + _timeframe +  " : No signal now : " + dtctx)
    return False

