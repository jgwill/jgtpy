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
instruments = "GBP/USD,AUD/USD,EUR/USD,SPX500,XAU/USD,USD/CAD,USD/JPY,EUR/CAD,AUD/CAD"
instruments = "AUD/USD,EUR/USD,SPX500,XAU/USD,USD/CAD,USD/JPY,EUR/CAD,AUD/CAD"

instruments = "AUD/USD,EUR/USD,SPX500,XAU/USD"

timeframes = ["M1","W1","D1","H4", "H1","m15","m5"]
timeframes = ["W1","D1","H4", "H1","m15","m5"]
show_tabs = False;show_chart=True
perspectives = {}

for i in instruments.split(","):
  print(i)
  experiment_name = "Perspective_" + i.replace("/","-") 



  #timeframes = ["D1","H4", "H1"]
  figures = {}

  for t in timeframes:
    print(i,t )
    data=ah.prepare_cds_for_ads_data(i,t,300)
    f,ax = ads.plot_from_cds_df(data,i,t,show=show_chart)
    f.title= t
    figures[t] = f
    
  # Create a tabbed layout
  tabs = pn.Tabs()

  # Add a tab for each timeframe
  for t in timeframes:
    tabs.append((t,figures[t]))
    
  html_fname = i.replace("/","-") + ".html"
  html_output_path = "../jgtcharts/pto-pers-" + html_fname
  
  perspectives[i] = tabs
  tabs.save(html_output_path,embed=True)
  if show_tabs:
      tabs.show()
      
  print(html_output_path)


#%% 