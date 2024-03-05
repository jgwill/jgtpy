

#@STCGoal Aim to become the container for lighting JGTADS

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTADSRequest import JGTADSRequest
import JGTPDSP as pds
import JGTIDS as ids
import JGTCDS as cds
from jgtutils import jgtwslhelper as wsl
import pandas as pd

from JGTChartConfig import JGTChartConfig

import logging
_loglevel= logging.WARNING

# Create a logger object
l = logging.getLogger()
l.setLevel(_loglevel)

# Create a console handler and set its level
console_handler = logging.StreamHandler()
console_handler.setLevel(_loglevel)

# Create a formatter and add it to the console handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the console handler to the logger
l.addHandler(console_handler)



def read_csv(csv_fn):
    df=pd.read_csv(csv_fn)
    # try:
    #     df.set_index('Date', inplace=True)
    # except:
    #     pass
    try:
        df.drop(columns=['Unnamed: 0'],inplace=True)
    except:
        pass
    return df

#IN_CHART_BARS=300

def prepare_cds_for_ads_data(instrument:str, timeframe:str,tlid_range:str=None,cc:JGTChartConfig=None,crop_last_dt:str=None,use_fresh=False,use_cache_if_available=False,rq:JGTADSRequest=None):
    """
    Prepare CDS data for ADS (Analysis Data Service).

    Args:
        instrument (str): The instrument symbol.
        timeframe (str): The timeframe of the data.
        tlid_range (str, optional): The range of TLID to select. Defaults to None.
        cc (JGTChartConfig, optional): The chart configuration. Defaults to None.
        crop_last_dt (str, optional): The last date to crop the data. Defaults to None.
        use_fresh (bool, optional): Whether to use fresh data. Defaults to False.
        use_cache_if_available (bool, optional): Whether to use cache if available. Defaults to False.
        rq (JGTADSRequest, optional): The JGTADSRequest object. Defaults to None.
    Returns:
        pandas.DataFrame: The prepared ADS(CDS) data with Selected number of bars

    """
    if cc is None:
        cc = JGTChartConfig()
        
    #@STCIssue Deprecating this value for later 
    
    #print("AH:DEBUG::Tlid_range:",tlid_range)
    if tlid_range is not None:
        raise NotImplementedError("tlid_range is not implemented yet. We will use crop_last_dt instead.")
    #@STCGoal local retrieve data from cache if available or from WSL if not  (jgtfxcli)
        
    cache_data:bool=use_cache_if_available
    cache_dir = "cache"
    
    if cache_data:
        os.makedirs(cache_dir, exist_ok=True)

    fn =  instrument.replace("/", "-") + "_" + timeframe + ".csv"
    fnpath_cache = os.path.join(cache_dir,fn)
    #l.info("fnpath:"+ fnpath)
    
    
    
    # @STCIssue Even the Cache above could be moved to JGTCDS or Business Layer
    # @STCIssue: LOGICS Bellow should be moved to JGTCDS  cds.create_crop_dt(...) cds.create_crop_dt_selection(...) 


    nb_to_select = cc.nb_bar_to_retrieve

    if crop_last_dt is None:
        # Get Lastest DF
        selected = pds.getPH(instrument,timeframe,cc=cc,get_them_all=True,use_fresh=use_fresh,quote_count=nb_to_select)
    else:
        # Get Crop DF, assuming we require using FULL data
        # df = pds.getPH(instrument,timeframe,cc=cc,use_full=True,use_fresh=use_fresh)
        selected = pds.getPH_crop(instrument,timeframe,quote_count=nb_to_select,dt_crop_last=crop_last_dt)
        #df = df[df.index <= crop_last_dt]

        
    print("DEBUG:: nb_to_select:",nb_to_select)
    print("DEBUG:: len selected:", len(selected))
    
    # #Make sure we have enough bars to select
    # if nb_to_select < cc.min_bar_on_chart:
    #     # Some instrument/tf dont have enough bars to select
    #     nb_to_select = cc.min_bar_on_chart
    #     selected = df.copy()
    # else: 
    #     selected = df.iloc[-nb_to_select:].copy()
        
    data = cds.createFromDF(selected)
    if cache_data:
        data.to_csv(fnpath_cache)
    
    return prepare_cds_for_ads_data_from_cdsdf(
        data,
        instrument,
        timeframe,
        tlid_range,
        cc,
        crop_last_dt
    
    )


def prepare_cds_for_ads_data_from_cdsdf(data, instrument: str, timeframe: str, tlid_range: str = None, cc: JGTChartConfig = None, crop_last_dt: str = None):
    """
    Prepare CDS data for ADS data from CDS DataFrame.

    Args:
        data (DataFrame): The CDS DataFrame containing the data.
        instrument (str): The instrument name.
        timeframe (str): The timeframe of the data.
        tlid_range (str, optional): The TLID range. Defaults to None.
        cc (JGTChartConfig, optional): The JGTChartConfig object. Defaults to None.
        crop_last_dt (str, optional): The last date to crop the data. Defaults to None.

    Returns:
        DataFrame: The prepared CDS data for ADS.
    """
    nb_bars = len(data)
    if nb_bars > cc.nb_bar_on_chart:
        r = data.iloc[-cc.nb_bar_on_chart:].copy()
    else:
        r = data.copy()
    return r


# def prepare_cds_for_ads_data_from_cdsdf(data,instrument:str, timeframe:str,tlid_range:str=None,cc:JGTChartConfig=None,crop_last_dt:str=None):   
#     nb_bars = len(data)
#     #print("AH:Debug: nb_bar_on_chart:",nb_bar_on_chart)
#     #print("AH:Debug:nb_bars b4 prep ends well:",nb_bars)
#     if nb_bars> cc.nb_bar_on_chart:
#         r = data.iloc[-cc.nb_bar_on_chart:].copy()
#     else:
#         r= data.copy()
#     #len_r = len(r)
#     #print("AH:Debug:nb_bars after prep ends well:",len_r)
#     return r


def get(instrument:str, timeframe:str,tlid_range:str=None,cc:JGTChartConfig=None,crop_last_dt:str=None):
#(instrument,timeframe,nb_bar_on_chart=500,crop_last_dt:str=None):
  data = prepare_cds_for_ads_data(instrument, timeframe,tlid_range,cc,crop_last_dt)
  return data
#p=pds.getPH(instrument,timeframe)
