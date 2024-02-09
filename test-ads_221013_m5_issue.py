# FILEPATH: /b/Dropbox/jgt/drop/scn-SPX500__221013__plot.py
# %% Import
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


# %% M1
t = "M1"
M1, M1a, M1df = ads.plot(instrument, t, show=show, cc=cc)
print(instrument, t)
# %%
t = "W1"
w1, w1a, w1df = ads.plot(instrument, t, show=show, cc=cc)
print(instrument, t)

# %%
t = "D1"
d1, d1a, d1df = ads.plot(instrument, t, show=show, cc=cc)
print(instrument, t)
t = "H4"
h4, h4a, h4df = ads.plot(instrument, t, show=show, cc=cc)
print(instrument, t)
t = "H1"
h1, h1a, d1df = ads.plot(instrument, t, show=show, cc=cc)
print(instrument, t)
t = "m15"
m15, m15a, m15adf = ads.plot(instrument, t, show=show, cc=cc)

# %% m5
t = "m5"
m5, m5a, m5adf = ads.plot(instrument, t, show=show, cc=cc)


# %% Save charts in scn_chart_dir

# M1.savefig("M1.png")
# w1.savefig("w1.png")
# d1.savefig("d1.png")
# h4.savefig("h4.png")
# h1.savefig("h1.png")
# m15.savefig("m15.png")
# m5.savefig("m5.png")


def save_figures(figures, directory):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    for name, fig in figures.items():
        fig.savefig(os.path.join(directory, f"{name}.png"))


# Usage:
figures = {"M1": M1, "w1": w1, "d1": d1, "h4": h4, "h1": h1, "m15": m15}

save_figures(figures, scn_chart_dir)
# %%
