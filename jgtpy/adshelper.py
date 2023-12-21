

#@STCGoal Aim to become the container for lighting JGTADS

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import JGTPDSP as pds
import JGTIDS as ids
import JGTCDS as cds
import jgtwslhelper as wsl
import pandas as pd


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


def prepare_cds_for_ads_data(instrument, timeframe, nb_bar_on_chart, recreate_data=True):
    """
    Prepare CDS (Credit Default Swap) data for ADS (Automated Trading System).

    Args:
        instrument (str): The instrument symbol.
        timeframe (str): The timeframe of the data.
        nb_bar_on_chart (int): The number of bars to display on the chart.
        recreate_data (bool, optional): Whether to recreate the data. Defaults to True.

    Returns:
        pandas.DataFrame: The prepared CDS data.

    """
    cache_data=False
    cache_dir = "cache"
    if cache_data:
        os.makedirs(cache_dir, exist_ok=True)

    fn =  instrument.replace("/", "-") + "_" + timeframe + ".csv"
    fnpath = os.path.join(cache_dir,fn)
    l.info("fnpath:"+ fnpath)

    #%% Load data
    l.info("-----------------  CDS  -----------------")
    if recreate_data:
        try:
            df = pds.getPH(instrument,timeframe,nb_bar_on_chart)
        except:
            l.warning("Could not get DF, trying to run thru WSL the update")
            wsl.jgtfxcli(instrument, timeframe, nb_bar_on_chart+35)
            df = pds.getPH(instrument,timeframe,nb_bar_on_chart)
        # Select the last 400 bars of the data
        try:
            selected = df.iloc[-nb_bar_on_chart-120:].copy()
            selected.to_csv("output_ads_prep_data.csv")
        except:
            l.warning("Could not get DF, trying to run thru WSL the update")
            wsl.jgtfxcli(instrument, timeframe, nb_bar_on_chart+35)
            try:
                df = pds.getPH(instrument,timeframe,nb_bar_on_chart)
                selected = df.copy()
            except:
                l.warning("Twice :(Could not select the desired amount of bars, trying anyway with what we have")
                pass
            l.warning("Could not select the desired amount of bars, trying anyway with what we have")
            pass
        #print(selected)
        data = cds.createFromDF(selected)
        if cache_data:
            data.to_csv(fnpath)
    return data


def get(instrument,timeframe,nb_bar_on_chart=500):
  data = prepare_cds_for_ads_data(instrument, timeframe, nb_bar_on_chart)
  return data
#p=pds.getPH(instrument,timeframe)
