
# %% Imports
import sys
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

#%% Creating a default chart configuration
def create_default_chart_config():
    cc = JGTChartConfig.JGTChartConfig()
    cc.saucer_marker_size = 14
    cc.ac_signals_marker_size = 14
    cc.fig_ratio_x = 31
    cc.fig_ratio_y = 16
    cc.nb_bar_on_chart = 300
    cc.plot_style = "yahoo"
    return cc
  
#%% Pto Panel 240209



def generate_market_snapshots(instruments, timeframes, html_outdir_root, show_chart=False, show_tabs=False):
  timeframes = timeframes.split(",")
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
        fnout = html_outdir_root + "/" + povfn + ".png"
        fnoutcsv = html_outdir_root + "/" + povfn + ".cds.csv"
        f.savefig(fnout)
        _.to_csv(fnoutcsv)

      tabs = pn.Tabs(width=2500, height=1100)

      for t in timeframes:
        tabs.append((t, figures[t]))

      if show_tabs:
        tabs.show()

      tabs.title = i

      html_fname = i.replace("/", "-") + ".html"
      html_output_filepath = f"{html_outdir_root}/pto-pers-" + html_fname

      tabs.save(html_output_filepath, embed=True)

      perspectives[i] = tabs

      ptabs.append((i, tabs))
    except:
      print("An error occurred while processing:", i)
      pass

  full_html_output_filepath = f"{html_outdir_root}/pto-full.html"
  print(full_html_output_filepath)

  ptabs.save(full_html_output_filepath, embed=True)