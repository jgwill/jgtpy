# %% Imports
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import panel as pn

import matplotlib.pyplot as plt

plt.rcParams["figure.max_open_warning"] = 100

import pandas as pd
from jgtpy import JGTADS as ads, adshelper as ah, JGTPDSP as pds, JGTCDS as cds
from jgtpy import JGTChartConfig

import tlid

# @STCGoal An online Platform to View charting

# %% Plot all charts in one operation
cc = JGTChartConfig.JGTChartConfig()
cc.saucer_marker_size = 14
cc.ac_signals_marker_size = 14
cc.fig_ratio_x = 31
cc.fig_ratio_y = 16
cc.nb_bar_on_chart = 300
cc.plot_style = "yahoo"


# %% The Experiment

instruments = "GBP/USD,AUD/USD,EUR/USD,SPX500,XAU/USD,USD/CAD,USD/JPY,EUR/CAD,AUD/CAD"
instruments = "GBP/USD,AUD/USD,EUR/USD,SPX500,XAU/USD,USD/CAD,USD/JPY,EUR/CAD,AUD/CAD"
instruments = (
    "AUS200,GBP/USD,AUD/USD,EUR/USD,SPX500,XAU/USD,USD/CAD,USD/JPY,EUR/CAD,AUD/CAD"
)


# Read the INSTRUMENTS variable from the environment or use the default value
instruments = os.getenv("I", instruments)
print(instruments)


defaulttimeframes = "M1,W1,D1,H8,H4,H1,m15,m5"
# Read the TIMEFRAMES variable from the environment or use the default value
timeframes = os.getenv("T", defaulttimeframes).split(",")
print(timeframes)


ldirdef = "./charts"
o = os.getenv("LDIR", ldirdef)
html_outdir_root = o

show_tabs = False
show_chart = False

perspectives = {}
ptabs = pn.Tabs(width=2550, height=1150)

for i in instruments.split(","):
    try:
        print(f"-------------{i}-------------------")

        figures = {}
        success = False
        for t in timeframes:
            print(i, t)
            f, ax, _ = ads.plot(i, t, show=show_chart, cc=cc)
            f.title = t
            figures[t] = f
            povfn = i.replace("/", "-") + "_" + t
            fnout = o + "/" + povfn + ".png"
            fnoutcsv = o + "/" + povfn + ".cds.csv"
            f.savefig(fnout)
            _.to_csv(fnoutcsv)

        # Create a tabbed layout
        # @STCIssue Ratio is different between this and CC
        tabs = pn.Tabs(width=2500, height=1100)

        # Add a tab for each timeframe
        for t in timeframes:
            tabs.append((t, figures[t]))

        if show_tabs:
            tabs.show()

        tabs.title = i

        html_fname = i.replace("/", "-") + ".html"
        html_output_filepath = f"{html_outdir_root}/pto-pers-" + html_fname

        # perspectives[i] = tabs
        tabs.save(html_output_filepath, embed=True)

        perspectives[i] = tabs

        ptabs.append((i, tabs))
    except:
        print("An error occurred while processing:", i)
        pass

# %% Full perspective with more than 1 instrument

full_html_output_filepath = f"{html_outdir_root}/pto-full.html"
print(full_html_output_filepath)

ptabs.save(full_html_output_filepath, embed=True)

# %%
