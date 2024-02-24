
# %% Imports
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

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


#support crop_last_dt="2022-10-13 13:45:00"
def generate_market_snapshots(instruments:str, timeframes:str, html_outdir_root:str=None,cc:JGTChartConfig=None,crop_last_dt:str=None, show_chart:bool=False, show_tabs:bool=False,width:int=2550, height:int=1150,save_fig_image:bool=True,save_cds_data:bool=True):
  if cc is None:
    cc = create_default_chart_config()
  if html_outdir_root is None:
    # Read the environment variable
    jgtpy_data_dir = os.environ.get("JGTPY_DATA")

    # Check if the environment variable is set
    if jgtpy_data_dir is not None:
      # Join the environment variable with "charts" to create a new directory path
      scn_chart_dir = os.path.join(jgtpy_data_dir, "charts")
      
      # Create the directory if it doesn't exist
      os.makedirs(scn_chart_dir, exist_ok=True)
      
      # Set html_outdir_root to the new directory
      html_outdir_root = scn_chart_dir
    else:
      print("Environment variable JGTPY_DATA is not set. Default to ./charts.")
      html_outdir_root = "./charts"
  timeframes = timeframes.split(",")
  perspectives = {}
  ptabs = pn.Tabs(width=width, height=height)

  for i in instruments.split(","):
    try:
      print(f"-------------{i}-------------------")

      figures = {}
      success = False
      for t in timeframes:
        print(i, t)
        f, ax, _ = ads.plot(i, t, show=show_chart, cc=cc, crop_last_dt=crop_last_dt,plot_ao_peaks=True)
        f.title = t
        figures[t] = f
        fnout, fnoutcsv = _mk_fnoutputs(html_outdir_root, i, t)
        
        if save_fig_image:        
          f.savefig(fnout)
        if save_cds_data:
          _.to_csv(fnoutcsv)

      tabs = pn.Tabs(width=width, height=height)

      for t in timeframes:
        tabs.append((t, figures[t]))

      if show_tabs:
        tabs.show()
        
      
      if crop_last_dt is not None:
        #cldt_fnstr=crop_last_dt.replace("/","-").replace(" ","_").replace(":","") 
        cldt_fnstr=tlid.strdt(crop_last_dt)
        tabs.title = i + " - " + crop_last_dt
        html_fname = i.replace("/", "-")+"_"+ cldt_fnstr + ".html"
      else:
        cldt_fnstr =tlid.get_minutes()
        tabs.title = i
        html_fname = i.replace("/", "-") + ".html"
      print(html_fname)
      
      html_output_filepath = f"{html_outdir_root}/pto-mksg-" + html_fname

      tabs.save(html_output_filepath, embed=True)

      perspectives[i] = tabs

      ptabs.append((i, tabs))
    except:
      print("An error occurred while processing:", i)
      pass

  full_html_output_filepath = f"{html_outdir_root}/pto-all-mksg.html"
  print(full_html_output_filepath)

  ptabs.save(full_html_output_filepath, embed=True)
  print("Saved:", full_html_output_filepath)

def _mk_fnoutputs(html_outdir_root, i, t):
    povfn = i.replace("/", "-") + "_" + t
    fnout = html_outdir_root + "/" + povfn + ".png"
    fnoutcsv = html_outdir_root + "/" + povfn + ".cds.csv"
    return fnout,fnoutcsv
