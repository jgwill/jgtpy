
#todo expose only the required functions to run CDS

## Requirement:   

"""
* Generate the CDS to file
* --@STCIssue Parse the CDS and get Valid signal (not fully implemented)

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
from jgtutils.jgtpov import get_higher_tf_by_level
from jgtutils.jgtos import get_data_path,mk_fullpath
from jgtutils import jgtconstants as c

def createCDSRequestFromArgs(args, instrument, timeframe):
    rq = JGTCDSRequest()
    rq.instrument = instrument
    rq.keep_bid_ask = args.keepbidask
    rq.timeframe = timeframe
    rq.quotescount = args.quotescount
    rq.use_fresh = args.fresh if args.fresh else False
    rq.use_full = args.full if args.full else False
    rq.gator_oscillator_flag = (
        args.gator_oscillator_flag if args.gator_oscillator_flag else False
    )
    rq.mfi_flag = args.mfi_flag if args.mfi_flag else False
    rq.balligator_flag = args.balligator_flag if args.balligator_flag else False
    rq.balligator_period_jaws = args.balligator_period_jaws
    rq.largest_fractal_period = args.largest_fractal_period
    rq.verbose_level = args.verbose
    return rq


def get(instrument,timeframe,use_full=False,use_fresh=True,quiet=True):
    """
    Generate the CDS to file
    """
    # Parse command line arguments
    # args = parse_args()
    # instrument = args.instrument
    # timeframe = args.timeframe

    # Create CDS request
    rq = JGTCDSRequest()
    rq.instrument = instrument
    rq.timeframe = timeframe
    rq.use_full = use_full
    rq.use_fresh = use_fresh

    # Create CDS
    return cds.create2(rq,quiet=quiet)



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


def _get_zone_from_cdf(_cdf):
  return _cdf[c.ZCOL].tail(1).values[0]

def _get_zone_index_from_cdf(_cdf):
  return _cdf[c.ZCOL].tail(1).index[0]

def zone_update(i,t,quiet=True,to_json=False): # We expect it to be saved in the zone folder
  cdf=get(i,t)
  return zone_update_from_cdf(i,t,cdf,quiet=quiet,to_json=to_json)

def zone_update_from_cdf(i,t,cdf,quiet=True,to_json=False): # We expect it to be saved in the zone folder  
  zone=_get_zone_from_cdf(cdf)
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

def read_zone_to_json(i, t):
  return zone_read(i, t, to_json=True)



#read zone and higher timeframe level
def zone_read_up(i,t,level=1,quiet=False,to_json=False):
  res={}
  # cur_zdata=read_zone(i,t).to_dict(orient="records")
  zone_data = zone_read(i,t,add_tf_key=False)
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
      zone_data["zint"]=1 if zone_data[c.ZCOL].values[0] == "green" else -1 if zone_data[c.ZCOL].values[0] == "red" else 0
    
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

