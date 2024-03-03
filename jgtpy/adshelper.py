

#@STCGoal Aim to become the container for lighting JGTADS

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
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

def prepare_cds_for_ads_data(instrument:str, timeframe:str,tlid_range:str=None,cc:JGTChartConfig=None,crop_last_dt:str=None):
    """
    Prepare CDS data for ADS (Analysis Data Service).

    Args:
        instrument (str): The instrument symbol.
        timeframe (str): The timeframe of the data.
        tlid_range (str, optional): The range of TLID to select. Defaults to None.
        cc (JGTChartConfig, optional): The chart configuration. Defaults to None.
        crop_last_dt (str, optional): The last date to crop the data. Defaults to None.
        
    Returns:
        pandas.DataFrame: The prepared CDS data with Selected number of bars

    """
    if cc is None:
        cc = JGTChartConfig()
        
    #@STCIssue Deprecating this value for later 
    
    #print("AH:DEBUG::Tlid_range:",tlid_range)
    if tlid_range is not None:
        raise NotImplementedError("tlid_range is not implemented yet. We will use crop_last_dt instead.")
    #@STCGoal local retrieve data from cache if available or from WSL if not  (jgtfxcli)
        
    cache_data:bool=False
    cache_dir = "cache"
    if cache_data:
        os.makedirs(cache_dir, exist_ok=True)

    fn =  instrument.replace("/", "-") + "_" + timeframe + ".csv"
    fnpath = os.path.join(cache_dir,fn)
    l.info("fnpath:"+ fnpath)

    # @STCIssue: Crop Last Dt out of range should use FULL
    
    try:
        df = pds.getPH(instrument,timeframe,cc=cc,get_them_all=True)
   
        if crop_last_dt is not None:
            df = df[df.index <= crop_last_dt]
        tst_len_df = len(df)
        
        if tst_len_df < cc.nb_bar_to_retrieve:
            l.warning(f"Data length is less than {cc.nb_bar_to_retrieve}, trying to use full storage")
            df = pds.getPH(instrument,timeframe,cc=cc,use_full=True)
        tst_len_df = len(df)
        
        if crop_last_dt is not None:
            df = df[df.index <= crop_last_dt]
        tst_len_df = len(df)
        
    except:
        l.warning("Could not get DF, trying to run thru WSL the update")
        wsl.jgtfxcli(instrument, timeframe, cc.nb_bar_to_retrieve)
        df = pds.getPH(instrument,timeframe,cc.nb_bar_to_retrieve) #@STCIssue Limitation of full range to be given yo jgtfxcli
    # Select the last 400 bars of the data
    try:#@q Is the selected correspond to desirrd bars ?
        #Make sure we have enough bars to select
        nb_to_select = cc.nb_bar_to_retrieve
        if nb_to_select < cc.min_bar_on_chart:
            nb_to_select = cc.min_bar_on_chart
            selected = df.copy()
        else:
            selected = df.iloc[-nb_to_select:].copy()
        
        tst_len_df = len(df)
        #selected.to_csv("output_ads_prep_data.csv")
    except:
        l.warning("Could not get DF, trying to run thru WSL the update")
        try:        
            wsl.jgtfxcli(instrument, timeframe, cc.nb_bar_to_retrieve)
        except:
                
            try:
                df = pds.getPH(instrument,timeframe,cc.nb_bar_to_retrieve)
                selected = df.copy()
            except:
                l.warning("Twice :(Could not select the desired amount of bars, trying anyway with what we have")
                pass
        l.warning("Could not select the desired amount of bars, trying anyway with what we have")
        pass
    #print(selected)
    len_selected = len(selected)
    #print("Len_selected:",len_selected)
    #print(selected.tail(1))
    #print("---------------")
    data = cds.createFromDF(selected)
    if cache_data:
        data.to_csv(fnpath)
    
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
