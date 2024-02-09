#%% INSTALLER
#%pip install jgtapy seaborn panel

# %% Import packages
from jgtpy import JGTADS as ads,adshelper as ah
from jgtpy import JGTPDSP as pds
from jgtpy import JGTChartConfig 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

#%% Set data path

print(os.getenv("JGTPY_DATA"))

instrument = "GBP/CAD"
instrument = "SOYF"
instrument = "SPX500"
instrument = "WHEATF"
t="M1"
# %% Load data and plot all in one operation
show=True
#m1p=pds.getPH(instrument, "M1")

#%% Plot all charts in one operation
cc = JGTChartConfig.JGTChartConfig()
cc.saucer_marker_size = 14;cc.ac_signals_marker_size=14
cc.fig_ratio_x = 24
cc.fig_ratio_y = 16
cc.nb_bar_on_chart = 300
cc.plot_style = "yahoo"

#%% M1, does data preparation works for TF ?
df = pds.getPH(instrument,t,cc=cc)
df # it plained loaded
#%% #@STCIssue NOTWORKING ah.prepare_cds_for_ads_data
data = ah.prepare_cds_for_ads_data(instrument, t,cc=cc)
    
    
#%% Manual Plot using the ads module
M1, M1a,M1df = ads.plot(instrument, t, show=show,cc=cc)





#%% M1
t="M1";M1, M1a,M1df = ads.plot(instrument, t, show=show,cc=cc)
print(instrument,t)
#%% 
t="W1";w1, w1a,w1df = ads.plot(instrument, t, show=show,cc=cc)
print(instrument,t)
