 
 
#%% IMPORTS
from jgtpy import JGTChartConfig , adshelper as ah

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
print(os.getenv("JGTPY_DATA"))


#%% INstruments + tf
instrument = "EUR/USD"
instrument = "XAU/USD"
instrument = "SPX500"
t="M1"

#%% Plot all charts in one operation
cc = JGTChartConfig.JGTChartConfig()
cc.saucer_marker_size = 14;cc.ac_signals_marker_size=14
cc.fig_ratio_x = 24
cc.fig_ratio_y = 16
cc.nb_bar_on_chart = 300
cc.plot_style = "yahoo"

#%% Load data and plot all in one operation
#M1c, M1a = ads.plot_from_pds_df(m1p,instrument, "M1", show=show)

data = ah.prepare_cds_for_ads_data(instrument, t,cc=cc)

count_test = len(data)

print("--------------------------------")
print("count_test:",str(count_test))
print("nbbar:",str(cc.nb_bar_on_chart))
print(" ----- We expect the two above values to be equal -----")



#%% Another TF
wt="W1"


wdata = ah.prepare_cds_for_ads_data(instrument, wt,cc=cc)

count_test = len(wdata)

print("--------------------------------")
print("count_test:",str(count_test))
print("nbbar:",str(cc.nb_bar_on_chart))
print(" ----- We expect the two above values to be equal -----")


#%% Plot
from jgtpy import JGTADS as ads

f,x,dfsrc = ads.plot(instrument, t, show=False, cc=cc)

#%%
f

#%%
ads.plot(instrument, wt, show=True, cc=cc)

#%%