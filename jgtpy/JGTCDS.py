# %%

import jgtpy.JGTPDS as pds
import jgtpy.JGTIDS as ids

import pandas as pd
import os

def startSession():
  pds.connect()
  
def stopSession():
  pds.dis
# %%
def create(instrument,timeframe,nb2retrieve=335,stayConnected=False,quiet=True):
  """Create CDS with Fresh Data

  Args:
      instrument (str): symbol
      timeframe (str): TF
      nb2retrieve (int, optional): nb bar to retrieve. Defaults to 335.
      stayConnected (bool, optional): Leave FXCMPY connected. Defaults to False.
      quiet (bool,optional): Output quiet

  Returns:
      pandas.DataFrame: CDS DataFrame
  """
  pds.stayConnected=stayConnected
  df=pds.getPH(instrument,timeframe,nb2retrieve,with_index=False,quiet=quiet)
  dfi=ids.ids_add_indicators(df,quiet=quiet)
  dfi=ids.cds_add_signals_to_indicators(dfi,quiet=quiet)
  dfi=ids.jgti_add_zlc_plus_other_AO_signal(dfi,quiet=quiet)
  dfi=ids.pds_cleanse_original_columns(dfi,quiet=quiet)
  dfi =ids.__ids_cleanse_ao_peak_secondary_columns(dfi,quiet=True)
  return dfi

#createByRange
def createByRange(instrument,timeframe,start,end,stayConnected=False,quiet=True):
  """Create CDS with Fresh Data

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
  dfi=ids.ids_add_indicators(df,quiet=quiet)
  dfi=ids.cds_add_signals_to_indicators(dfi,quiet=quiet)
  dfi=ids.jgti_add_zlc_plus_other_AO_signal(dfi,quiet=quiet)
  dfi=ids.pds_cleanse_original_columns(dfi,quiet=quiet)
  dfi =ids.__ids_cleanse_ao_peak_secondary_columns(dfi,quiet=True)
  return dfi

def createFromDF(df,quiet=True):
  dfi=ids.ids_add_indicators(df,quiet=quiet)
  dfi=ids.cds_add_signals_to_indicators(dfi,quiet=quiet)
  dfi=ids.jgti_add_zlc_plus_other_AO_signal(dfi,quiet=quiet)
  dfi=ids.pds_cleanse_original_columns(dfi,quiet=quiet)
  dfi =ids.__ids_cleanse_ao_peak_secondary_columns(dfi,quiet=True)
  return dfi

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
  r= _df#['High','Low','ao','fdb','ac']
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
  isfdb = pa['fdb'][0]  != 0.0
  fdb = pa['fdb']
  dtctx = pa['Date']
  if isfdb:
    print(_instrument + "_" + _timeframe + " : We Have a Signal : " + dtctx)
    return True
  else:
    print(_instrument + "_" + _timeframe +  " : No signal now : " + dtctx)
    return False

