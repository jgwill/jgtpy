#%% Imp.orts
import os
#@URIR B:\Dropbox\jgt\drop\rl_comet_jgt_chart03.py


import plotly.graph_objects as go
from plotly.subplots import make_subplots
import panel as pn


import pandas as pd
from jgtpy import JGTADS as ads,adshelper as ah, JGTPDSP as pds,JGTCDS as cds
import tlid
#@STCGoal An online Platform to View charting



#%% The Experiment
i="SPX500"
i="EUR/USD"
i="AUD/USD"
i="XAU/USD"

experiment_name = "Perspective_" + i.replace("/","-") 

#%% Print current working directory
print(os.getcwd())

#%% Load Many POV

timeframes = ["M1","W1","D1","H4", "H1","m15","m5"]
#timeframes = ["D1","H4", "H1"]
figures = {}

for t in timeframes:
  # fnamebase = i.replace("/","-") + "_" + t
  # fname = fnamebase + ".csv"
  # # try: 
  # #   DATA_ROOT = os.getenv("JGTPY_DATA")
  # # except:
  # DATA_ROOT = "../data"
  # #if not exists(DATA_ROOT), use ../../data
  # if not os.path.exists(DATA_ROOT):
  #   DATA_ROOT = "../../data"
  # fpath = DATA_ROOT + "/cds/" + fname
  # print(fpath)
  # data = pd.read_csv(fpath,index_col=0,parse_dates=True)
  # Plot some data expecting to see them in the experiment
  # f,ax = ads.plot_from_cds_df(data,i,t,show=True)
  data=ah.prepare_cds_for_ads_data(i,t,300)
  f,ax = ads.plot_from_cds_df(data,i,t,show=True)
  f.title= t
  figures[t] = f
  

#%% TABS


# Create a tabbed layout
tabs = pn.Tabs()

# Add a tab for each timeframe
for t in timeframes:
  tabs.append((t,figures[t]))
  

#%% Set the font size of the tab names

# Wrap the tabs object with an HTML object and set the font size of the tab names
#tabs_div = pn.panel(tabs, sizing_mode="stretch_width", style={"description_width": "initial", "font_size": "22pt"})


#%% OUTPUT
  #tabs[int(t[-2:])] = figures[t]
html_fname = i.replace("/","-") + ".html"
html_output_path = "pto-pers-" + html_fname



tabs.save(html_output_path,embed=True)
print(html_output_path)





# %% VIEW TABS
pn.extension()
tabs.show()


# %%
