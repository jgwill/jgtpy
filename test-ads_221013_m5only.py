#%% imports

import os
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from jgtpy import JGTADS as ads
from jgtpy import JGTChartConfig

# %% Set JGTPY_DATA to the scn
scntlid = "240209"
scntlid = "221013"
scn_root_dir = f"/b/Dropbox/jgt/drop/data/scn/SPX500_{scntlid}"

scn_jgtpy_data = os.path.join(scn_root_dir, "data")
os.environ["JGTPY_DATA"] = scn_jgtpy_data

scn_chart_dir = os.path.join(scn_root_dir, "charts")
os.makedirs(scn_chart_dir, exist_ok=True)

# %% Show the data directory
print(os.environ["JGTPY_DATA"])

# %%
# Plot timeframes of the data using ads

instrument = "SPX500"

# %% Load data and plot all in one operation
show = True
# m1p=pds.getPH(instrument, "M1")

# %% Plot all charts in one operation
cc = JGTChartConfig.JGTChartConfig()
cc.saucer_marker_size = 14
cc.ac_signals_marker_size = 14
cc.fig_ratio_x = 24
cc.fig_ratio_y = 16
cc.nb_bar_on_chart = 300
cc.plot_style = "yahoo"

# %% m5
t = "m5"
crop_last_dt="2022-10-13 13:45:00"
m5, m5a, m5adf = ads.plot(instrument, t, show=show, cc=cc,crop_last_dt=crop_last_dt)

# %%
