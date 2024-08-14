"""
This module, JGTCDSSvc.py, is part of a larger application designed to interact with the Chaos Data Service (CDS). It includes functionality to create data requests for financial market data based on user-specified parameters. The module handles the initialization and configuration of these data requests, leveraging the Chaos Data Service's capabilities to fetch and process financial data.

Imports:
- warnings: Used to ignore FutureWarning messages that might arise.
- sys, os: For path manipulations and system-level operations.
- pandas (pd): For handling data structures and operations on them.
- json: For parsing JSON data.

The module also imports specific functionalities from other parts of the application:
- JGTCDS: A module that likely contains core functionalities related to the Chaos Data Service.
- JGTCDSRequest: A class definition for creating request objects to interact with the CDS.
- jgtutils.jgtpov: Utilities for processing or obtaining higher timeframes from given data.
- jgtutils.jgtos: Operating system utilities, such as path getters and creators.
- jgtutils.jgtconstants (c): Constants used throughout the application, possibly including default values or configuration settings.



Overall, this module serves as a bridge between the user's command-line inputs and the Chaos Data Service, enabling the dynamic creation and configuration of data requests based on user preferences and requirements.
"""

import warnings

# Ignore FutureWarning
warnings.simplefilter(action="ignore", category=FutureWarning)

import sys
import os
import pandas as pd
import json


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import JGTCDS as cds
from JGTCDSRequest import JGTCDSRequest
from jgtutils.jgtpov import get_higher_tf_by_level,get_higher_tf_array
from jgtutils.jgtos import get_data_path,mk_fullpath
from jgtutils import jgtconstants as c

from jgtutils.jgtconstants import NB_BARS_BY_DEFAULT_IN_CDS


def set_rq_defaults(rq): #@STCIssue We would migrate to use jgtutils/jgtclirqdata.py
    rq.keep_bid_ask = True
    if not rq.use_full and rq.quotescount == -1:
      rq.quotescount = NB_BARS_BY_DEFAULT_IN_CDS
    rq.viewpath = False
    rq.gator_oscillator_flag = False
    rq.mfi_flag = True
    rq.balligator_flag = True
    rq.talligator_flag = True
    rq.dropna_volume = True
    
    if rq.timeframe=="M1":
      rq.talligator_flag = False
      
    rq.balligator_fix_quotescount()
    rq.talligator_fix_quotescount()
    return rq

    
    
def new_rq_default(instrument,timeframe,use_fresh=True,use_full=False,quotescount=-1):
    rq = JGTCDSRequest()
    rq.instrument = instrument
    rq.timeframe = timeframe
    rq.quotescount = quotescount
    rq.use_full = use_full
    rq.use_fresh = use_fresh
    rq=set_rq_defaults(rq)
    # if rq.talligator_flag:
    #   print("Talligator flag is set")
    return rq

def create(rq: JGTCDSRequest):
    cdf= cds.create2(rq)
    return cdf

def get(instrument,timeframe,use_full=False,use_fresh=True,quotescount=-1,quiet=True,dont_write_cds=False):
    """
    Generate the CDS to file
    """
    # Parse command line arguments
    # args = parse_args()
    # instrument = args.instrument
    # timeframe = args.timeframe

    # Create CDS request
    #@STCIssue SHOULD Use JGTCDSRequest !!!
    rq = new_rq_default(instrument,timeframe,use_fresh=use_fresh,use_full=use_full,quotescount=quotescount)

    # Create CDS
    cdf= cds.create2(rq,quiet=quiet)
    if not dont_write_cds:
      cds.writeCDS(instrument, timeframe, use_full, cdf)
      #cds.writeCDS(cdf=cdf,instrument=instrument,timeframe=timeframe,use_full=use_full,quotescount=quotescount,quiet=quiet)
    return cdf

def read(instrument,timeframe,use_full=False,quotescount=-1,quiet=True):
  try:
    cdf= cds.readCDSFile(instrument,timeframe,use_full=use_full,quote_count=quotescount,quiet=quiet)
  except:
    cdf=None
  if cdf is None:
    print("CDS Could not read, so we create it....",timeframe)
    cdf=get(instrument,timeframe,use_full=use_full,quotescount=quotescount,quiet=quiet)
  #print("CDSSvc Read: cdf len: ", len(cdf))
  return cdf

import concurrent.futures

# Move the get_cdf function to the top level
def get_cdf(i, t, tf, use_full, use_fresh, quiet, quotescount,force_read=False):
  if use_fresh:
    force_read=False
  _f=":f" if use_full else ""
  if force_read:
    print("   CDSSvc Read: ",i," ", tf, "/", t, _f,"\n")
    return tf, read(i, tf, use_full=use_full, quotescount=quotescount, quiet=quiet)
  else:
    print("CDSSvc Create: ",i," ", tf, "/", t, _f,"\n")
    return tf, get(i, tf, use_full=use_full, use_fresh=use_fresh, quiet=quiet, quotescount=quotescount)

def get_higher_cdf_datasets(i, t, use_full=False, use_fresh=True, quiet=True, quotescount=-1,force_read=False):
  if not use_fresh and not force_read:
    force_read=True # We force read if not use_fresh
    
  tf_array = get_higher_tf_array(t)
  if not quiet:
    print("Higher TF Array: ", tf_array)
  res = {}

  # Use a ProcessPoolExecutor to run the function in parallel for each tf in tf_array
  with concurrent.futures.ProcessPoolExecutor() as executor:
    futures = {executor.submit(get_cdf, i, t, tf, use_full, use_fresh, quiet, quotescount,force_read) for tf in tf_array}

    for future in concurrent.futures.as_completed(futures):
      tf, cdf = future.result()
      res[tf] = cdf

  return res

def get_higher_cdf_datasets__ThreadPoolExecutor(i, t, use_full=False, use_fresh=True, quiet=True, quotescount=NB_BARS_BY_DEFAULT_IN_CDS):
  tf_array = get_higher_tf_array(t)
  if not quiet:
    print("Higher TF Array: ", tf_array)
  res = {}

  # Define a function to be run in parallel
  def get_cdf(tf):
    print("CDSSvc Get: ", tf, " of : ", t," for: ",i)
    return tf, get(i, tf, use_full=use_full, use_fresh=use_fresh, quiet=quiet, quotescount=quotescount)

  # Use a ThreadPoolExecutor to run the function in parallel for each tf in tf_array
  with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(get_cdf, tf) for tf in tf_array}

    for future in concurrent.futures.as_completed(futures):
      tf, cdf = future.result()
      res[tf] = cdf

  return res

def get_higher_cdf_datasets_no_concurrence(i,t,use_full=False,use_fresh=True,quiet=True,quotescount=NB_BARS_BY_DEFAULT_IN_CDS):
  tf_array=get_higher_tf_array(t)
  if not quiet:
    print("Higher TF Array: ",tf_array)
  res={}
  for tf in tf_array:
    #if not quiet:
    print("CDSSvc Get: ",tf," of : ",t)
    cdf=get(i,tf,use_full=use_full,use_fresh=use_fresh,quiet=quiet,quotescount=quotescount)
    res[tf]=cdf
    #res.append(cdf)
  return res

def get_higher_cdf(i,t,_level=1,default_timeframes = "M1,W1,D1,H4,H1,m15,m5",quiet=True):
  if default_timeframes=="T":# try read the os var "T"
    default_timeframes=os.getenv("T","M1,W1,D1,H4,H1,m15,m5")
    if not quiet:
       print("default timeframes read from env: ",default_timeframes)
  
  if _level==0:
    return get(i,t),t # Current
  else:
    htf=get_higher_tf_by_level(t,_level,default_timeframes)
    if not quiet:
       print("Higher TF: ",htf," of : ",t)
    if htf==None:
      return None,None # No higher TF
    

    hdf=get(i,htf)
    
    return hdf,htf


def zone_get_value_from_cdf(_cdf):
  return _cdf[c.ZCOL].tail(1).values[0]

def _get_zone_index_from_cdf(_cdf):
  return _cdf[c.ZCOL].tail(1).index[0]

def zone_update(i,t,quiet=True,to_json=False): # We expect it to be saved in the zone folder
  cdf=get(i,t)
  return zone_update_from_cdf(i,t,cdf,quiet=quiet,to_json=to_json)

def zone_update_from_cdf(i,t,cdf,quiet=True,to_json=False): # We expect it to be saved in the zone folder  
  zone=zone_get_value_from_cdf(cdf)
  if not quiet:
    print("Zone: ",zone)
  
  zone_data = zone__from_cdf_to_zonedata(cdf)
  # Save the zone
  fpath=zone_save_data(i,t,zone_data)
  if to_json:
    r= {}
    r["path"]=fpath
    
    # try:
    #    r["data"]=zone_data
    # except:
    #   r["data"]=zone_data

    return json.dumps(r)
  return fpath,zone_data

#@STGoal Current and Higher timeframes zone are updated.
def zone_update_higher(i,t,level=1,quiet=True,to_json=False): # We expect it to be saved in the zone folder
  res={}
  current_path,cur_zone_data = zone_update(i,t,quiet=quiet)
  cur={}
  cur["data"]=cur_zone_data
  cur["path"]=current_path
  res[t]=cur
  
  if level>0:
    # #Update the first level zone
    # if not quiet:print("Update the first zone level:",t)

    # htf1=get_higher_tf_by_level(t,level)
    # print("Higher TF: ",htf1," of : ",t)
    # if htf1==None:
    #   return res
    # tf1_path=zone_update(i,htf1)
    # res.append(tf1_path)
    #iterate thru level 
    for ii in range(1,level+1):
      htf=get_higher_tf_by_level(t,ii)
      if htf is None:
        continue
      if not quiet:print(f"Update the {ii} zone level ({t}/{htf})")
      tf_path,_zd=zone_update(i,htf,quiet=quiet,to_json=to_json)
      hz={}
      hz["data"]=_zd
      hz["path"]=tf_path
      res[htf]=hz
  if to_json:
    return json.dumps(res)
  return res
  
# Get the zone from data store
def zone_read(i,t,add_tf_key=True,to_json=False,add_instrument_key=False):
  data_path_zone = get_data_path("zone")
  fpath = mk_fullpath(i, t, "csv", data_path_zone)
  #if not exist fpath
  if not os.path.exists(fpath):
    print("No zone data found for ",i,t)
    print("Creating zone data for ",i,t)
    zone_update(i,t)
  zone_data=pd.read_csv(fpath)
  if add_tf_key:
    zone_data["t"]=t
  if add_instrument_key:
    zone_data["i"]=i
  if to_json:
    return df_to_json(zone_data)
  return zone_data



def df_to_json(df,row_id=0,orient='records'):
  json_str = df.to_json(orient=orient)
  json_obj = json.loads(json_str)
  return json_obj[row_id] if json_obj else None

def read_zone_to_json(i, t,add_instrument_key=False,add_tf_key=False):
  return zone_read(i, t, to_json=True,add_instrument_key=add_instrument_key,add_tf_key=add_tf_key)



#read zone and higher timeframe level
def zone_read_up(i,t,level=1,quiet=False,to_json=False,add_instrument_key=False,add_tf_key=False):
  res={}
  # cur_zdata=read_zone(i,t).to_dict(orient="records")
  zone_data = zone_read(i,t,add_tf_key=add_tf_key,add_instrument_key=add_instrument_key)
  cur_zdata=df_to_json(zone_data)
  res[t]=cur_zdata
  #res.append(current)
  if level>0:
    # #Update the first level zone
    # if not quiet:print("Read the first zone level:",t)

    # tf1=get_higher_tf_by_level(t,level)
    # print("Higher TF: ",tf1," of : ",t)
    # if tf1==None:
    #   return res
    # h1_zdata=read_zone(i,tf1)
    # res[tf1]=h1_zdata
    #iterate thru level 
    for ii in range(1,level+1):
      tf_ii=get_higher_tf_by_level(t,ii)
      if not quiet:print(f"Read the {ii} zone level ({t}/{tf_ii})")
      # hz_data=read_zone(i,tf_ii).to_dict(orient="records")
      hz_data=df_to_json(zone_read(i,tf_ii,add_tf_key=False))
      res[tf_ii]=hz_data
  if to_json:
    return json.dumps(res)
  return res


def zone__from_cdf_to_zonedata(cdf,add_zone_int=True): # expect to keep one column,last row
    zone_data=cdf.tail(1)
    #print(zone_data)
    #keep c.ZCOL in zone_data
    zone_data=zone_data[[c.ZCOL]]

    if add_zone_int:
      zone_data[c.ZONE_INT]=c.ZONE_BUY_ID if zone_data[c.ZCOL].values[0] == c.ZONE_BUY_STR else c.ZONE_SELL_ID if zone_data[c.ZCOL].values[0] == c.ZONE_SELL_STR else c.ZONE_NEUTRAL_ID
    
    return zone_data


def zone_save_data(instrument, timeframe, zone_data,save_json=True):
    data_path_zone = get_data_path("zone")
    fpath = mk_fullpath(instrument, timeframe, "csv", data_path_zone)
    # print(fpath)
    zone_data.to_csv(fpath, index=True)
    fpath_json = mk_fullpath(instrument, timeframe, "json", data_path_zone)
    
    if save_json:
      zone_data_json=df_to_json(zone_data)
      with open(fpath_json, 'w') as outfile:
          json.dump(zone_data_json, outfile)

    return fpath

