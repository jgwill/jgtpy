# %% Import packages
from jgtpy import JGTADS as ads
from jgtpy import JGTCDS as cds
from jgtpy import JGTPDSP as pds
from jgtpy import JGTChartConfig
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

print(os.getenv("JGTPY_DATA"))

instrument = "EUR/USD"
instrument = "XAU/USD"
instrument = "SPX500"
# %% Load data and plot all in one operation
show = True
dt_crop_last = "2020-03-01"  # Strong curve up SPX500 H4
keep_quote_count = 1500
t = "D1"
t = "H1"


# %% Plot all charts in one operation
cc = JGTChartConfig.JGTChartConfig()
cc.saucer_marker_size = 14
cc.fig_ratio_x = 24
cc.fig_ratio_y = 18
cc.plot_style = "yahoo"

jgtpy_data_full = os.getenv("JGTPY_DATA_FULL")
print(jgtpy_data_full)

# %%
df = cds.readCDSFile(
    instrument,
    t,
    quiet=False,
    use_full=True,
    dt_crop_last=dt_crop_last,
    quote_count=keep_quote_count,
)
# %%
df.tail(1)
df.to_csv("test.csv")
# %%
c,a,d = ads.plot(instrument, t, show=show,cc=cc)
d.to_csv("test2.csv")
# %%

c2, a2, d2 = ads.plot_from_cds_df(df, instrument, t, show=show, cc=cc)
# %%
