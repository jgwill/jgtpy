#%% Imp.orts
import os
#@URIR B:\Dropbox\jgt\drop\rl_comet_jgt_chart03.py


import plotly.graph_objects as go
from plotly.subplots import make_subplots
import panel as pn

import matplotlib.pyplot as plt
plt.rcParams['figure.max_open_warning'] = 100

import pandas as pd
from jgtpy import JGTADS as ads,adshelper as ah, JGTPDSP as pds,JGTCDS as cds
from jgtpy import JGTChartConfig 

import tlid
#@STCGoal An online Platform to View charting

#%% Plot all charts in one operation
cc = JGTChartConfig.JGTChartConfig()
cc.saucer_marker_size = 14;cc.ac_signals_marker_size=14
cc.fig_ratio_x = 31
cc.fig_ratio_y = 16
cc.nb_bar_on_chart = 300
cc.plot_style = "yahoo"


#%% The Experiment
i="SPX500"
i="EUR/USD"
i="AUD/USD"
i="XAU/USD"
instruments = "GBP/USD,AUD/USD,EUR/USD,SPX500,XAU/USD,USD/CAD,USD/JPY,EUR/CAD,AUD/CAD"
#instruments = "AUD/USD,EUR/USD,SPX500,XAU/USD,USD/CAD,USD/JPY,EUR/CAD,AUD/CAD"

#instruments = "USD/CAD,USD/JPY,EUR/CAD,AUD/CAD"
#instruments = "SPX500,XAU/USD"

timeframes = ["M1","W1","D1","H4", "H1","m15","m5"]
#timeframes = ["W1","D1","H4", "H1","m15","m5"]

html_outdir_root = "docs/charts"
html_outdir_root = "../jgtcharts/charts"

show_tabs = False;show_chart=False

perspectives = {}
ptabs = pn.Tabs(width=2550,height=1150)

for i in instruments.split(","):
  try:
    print(i)
    experiment_name = "Perspective_" + i.replace("/","-") 
    
    #timeframes = ["D1","H4", "H1"]
    figures = {}

    for t in timeframes:
      print(i,t )
      #data=ah.prepare_cds_for_ads_data(i,t,300)
      f,ax,_ = ads.plot(i,t,show=show_chart,cc=cc)
      f.title= t
      figures[t] = f
      
    # Create a tabbed layout
    tabs = pn.Tabs(width=2500,height=1100)

    # Add a tab for each timeframe
    for t in timeframes:
      tabs.append((t,figures[t]))
    
    if show_tabs:
        tabs.show()
    
    tabs.title = i
    
    
    html_fname = i.replace("/","-") + ".html"
    html_output_filepath = f"{html_outdir_root}/pto-pers-" + html_fname
    
    #perspectives[i] = tabs
    tabs.save(html_output_filepath,embed=True)
    
    
    
    perspectives[i] = tabs
    
    ptabs.append((i,tabs))
  except:
    print("An error occurred while processing:",i)
    pass

#%% Full perspective with more than 1 instrument

full_html_output_filepath = f"{html_outdir_root}/pto-full.html" 
print(full_html_output_filepath)
  
ptabs.save(full_html_output_filepath,embed=True)
  
#%% 