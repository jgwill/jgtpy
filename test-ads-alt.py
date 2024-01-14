#%% INSTALLER
#%pip install jgtapy seaborn panel

# %% Import packages
from jgtpy import JGTADS as ads
from jgtpy import JGTPDSP as pds
from jgtpy import JGTChartConfig 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

#%% Set data path

print(os.getenv("JGTPY_DATA"))

instrument = "EUR/USD"
instrument = "XAU/USD"
instrument = "SPX500"
instrument = "WHEATF"
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

#%% M1
t="M1";M1, M1a,M1df = ads.plot(instrument, t, show=show,cc=cc)
print(instrument,t)
#%% 
t="W1";w1, w1a,w1df = ads.plot(instrument, t, show=show,cc=cc)
print(instrument,t)
