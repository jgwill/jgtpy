#@title Plotly

#%% Imports
import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt
import mplfinance as mpf


import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

#import jgtpy
import JGTPDSP as pds
import JGTIDS as ids
from JGTIDS import getMinByTF
import JGTCDS as cds
import jgtwslhelper as wsl

warnings.filterwarnings("ignore", category=FutureWarning)

import os

#import kaleido
import plotly

import JGTConfig as jgtc


import plotly.graph_objects as go
import plotly.subplots as sp



#%% Logging

import logging
_loglevel= logging.WARNING

# Create a logger object
l = logging.getLogger()
l.setLevel(_loglevel)

# Create a console handler and set its level
console_handler = logging.StreamHandler()
console_handler.setLevel(_loglevel)

# Create a formatter and add it to the console handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the console handler to the logger
l.addHandler(console_handler)












cdtformat="%Y-%m-%d"




from jgtconstants import (
  sellingZoneColor,
  buyingZoneColor,
)

# %%
#@title INDICATOR's Data Frame Columns naming
# Import statements for jgtconstants.py variables


from jgtconstants import (
    indicator_currentDegree_alligator_jaw_column_name,
    indicator_currentDegree_alligator_teeth_column_name,
    indicator_currentDegree_alligator_lips_column_name,
    indicator_sixDegreeLarger_alligator_jaw_column_name,
    indicator_sixDegreeLarger_alligator_teeth_column_name,
    indicator_sixDegreeLarger_alligator_lips_column_name,
    indicator_AO_awesomeOscillator_column_name,
    indicator_zeroLineCross_column_name,
    indicator_ao_fractalPeakOfMomentum_column_name,
    indicator_ao_fractalPeakValue_column_name,
    indicator_AO_aboveZero_column_name,
    indicator_AO_bellowZero_column_name,
    indicator_AC_accelerationDeceleration_column_name,
    indicator_gatorOscillator_low_column_name,
    indicator_gatorOscillator_high_column_name,
    indicator_mfi_marketFacilitationIndex_column_name,
    indicator_fractal_high_degree2_column_name,
    indicator_fractal_low_degree2_column_name,
    indicator_fractal_high_degree3_column_name,
    indicator_fractal_low_degree3_column_name,
    indicator_fractal_high_degree5_column_name,
    indicator_fractal_low_degree5_column_name,
    indicator_fractal_high_degree8_column_name,
    indicator_fractal_low_degree8_column_name,
    indicator_fractal_high_degree13_column_name,
    indicator_fractal_low_degree13_column_name,
    indicator_fractal_high_degree21_column_name,
    indicator_fractal_low_degree21_column_name,
    indicator_fractal_high_degree34_column_name,
    indicator_fractal_low_degree34_column_name,
    indicator_fractal_high_degree55_column_name,
    indicator_fractal_low_degree55_column_name,
    indicator_fractal_high_degree89_column_name,
    indicator_fractal_low_degree89_column_name,
)


# %%
#@title SIGNAL's Data Frame Columns naming
# Import statements for jgtconstants.py variables

from jgtconstants import (
    signalCode_fractalDivergentBar_column_name,
    signalSell_fractalDivergentBar_column_name,
    signalBuy_fractalDivergentBar_column_name,
    signalSell_fractal_column_name,
    signalBuy_fractal_column_name,
    signal_zcol_column_name,
    signalSell_zoneSignal_column_name,
    signalBuy_zoneSinal_column_name,
    signalBuy_zeroLineCrossing_column_name,
    signalSell_zeroLineCrossing_column_name,
    signalSell_AC_deceleration_column_name,
    signalBuy_AC_acceleration_column_name,
    signalSell_saucer_column_name,
    signalBuy_saucer_column_name,
)

# if timeframe=='m5':
# 	cdtformat='%H:%M'
 


#@title JGT Plotting Functions
def jgtplt_createSubplots(rows=4,row_heights=[50,15,15],cols=1,shared_xaxes=True):
  return sp.make_subplots(rows=rows, cols=cols,row_heights=row_heights,shared_xaxes=shared_xaxes)

def addline2main(_fig,_data,xdata,name,color,width=1,opacity=0.5,row=1,col=1):
  _fig.add_trace(go.Scatter(
    x=xdata, y=_data, opacity=opacity,
    line=dict(color=color, width=width), name=name),
    row=row, col=col)
  return _fig
 
 
 #@title DEF Charting Function PTO 221025

#@title RESTORE RAnge break

def _ads_get_dt_break(dfsrc,_timeframe='',_cdtformat="%Y-%m-%d"):
  if _timeframe=='m5' or _timeframe == 'm1' or _timeframe =='mi1':
    _cdtformat='%H:%M'
  _dt_all = pd.date_range(start=dfsrc.index[0],end=dfsrc.index[-1])
  # retrieve the dates that ARE in the original datset
  _dt_obs = [d.strftime(_cdtformat) for d in pd.to_datetime(dfsrc.index)]
  # define dates with missing values
  _dt_breaks = [d for d in _dt_all.strftime("%Y-%m-%d").tolist() if not d in _dt_obs]
  return _dt_breaks


 
#@title Coloring the AO  
# df['aocolor'] = 'rgba(255, 0, 0, 1.0)'
# if df[[df[indicator_AO_awesomeOscillator_column_name]] > df[df['pao0']]:
#   df['aocolor'] = 'rgba(0, 255, 0, 1.0)'
# df.tail()

def retrieve_n_chart_pano(_instrument,_nb2retrieve=335,_cw =1050,_ch =1000,useDTBreaks=False):
  charts={}
  for _timeframe in jgtc.contextTimeframes:
    print('ADS is retrieving for: ' + _instrument + '_'+ _timeframe)
    _df=cds.create(_instrument,_timeframe,_nb2retrieve,True)
    f4=ads_chart_pto(_df,_timeframe,_cw,_ch,useDTBreaks)
    charts[_timeframe]= f4
  return charts

def retrieve_n_chart(_instrument,_timeframe,_nb2retrieve=335,_cw =1050,_ch =1000,useDTBreaks=False):
  print('ADS is retrieving for: ' + _instrument + '_'+ _timeframe)
  _df=cds.create(_instrument,_timeframe,_nb2retrieve)
  f4=ads_chart_pto(_df,_timeframe,_cw,_ch,useDTBreaks)
  return f4



def ads_chart_pto(dfsrc,_timeframe,_cw =1050,_ch =1000,useDTBreaks=False)-> plt.Figure:
  fdball =  dfsrc[dfsrc[signalCode_fractalDivergentBar_column_name]!=0 ] 
  fdbs = dfsrc[dfsrc[signalSell_fractalDivergentBar_column_name]==True]
  fdbb = dfsrc[dfsrc[signalBuy_fractalDivergentBar_column_name]==True]
  aocolor=dfsrc['aocolor'].values.tolist()
  
  zcolor=dfsrc[signal_zcol_column_name].values.tolist()
  #print(aocolor)
  #@title Arrays for Charting
  _dt_breaks=_ads_get_dt_break(dfsrc,_timeframe)
  _fdball=dfsrc[dfsrc[signalCode_fractalDivergentBar_column_name] != 0 ]
  _open_data = dfsrc['Open']
  _close_data = dfsrc['Close']
  _high_data = dfsrc['High']
  _low_data = dfsrc['Low']
  _ao_data = dfsrc[indicator_AO_awesomeOscillator_column_name]
  _ac_data = dfsrc[indicator_AC_accelerationDeceleration_column_name]
  #dates = _df['Date']
  _dates =dfsrc.index #dates are used as index, hope its ok
  _dates_fdball = fdball.index
  _dates_fdbs = fdbs.index
  _dates_fdbb = fdbb.index
  #print(dates)
  _fdbs_data = dfsrc[signalSell_fractalDivergentBar_column_name]
  _fdbb_data = dfsrc[signalBuy_fractalDivergentBar_column_name]
  _fs_data = dfsrc[signalSell_fractal_column_name]
  _fb_data = dfsrc[signalBuy_fractal_column_name]
  
  _zlc_data = dfsrc[indicator_zeroLineCross_column_name]
  _saucersell_data=dfsrc[signalSell_saucer_column_name]
  _saucerbuy_data=dfsrc[signalBuy_saucer_column_name]
  _zcol_data = dfsrc[signal_zcol_column_name]
  # fig = go.Figure(data=[go.Ohlc(x=dates,
  #                           open=open_data, high=high_data,
  #                           low=low_data, close=close_data)])
  # fig.show()
  # Plot OHLC on 1st subplot (using the codes from before)
  _f4 = sp.make_subplots(rows=3, cols=1,row_heights=[75,20,15],shared_xaxes=True)
                          #, specs=[[{'l': 0},{'r': 0}], [{'t': 0}, {'b': 0}]], shared_xaxes=True)
  mainrow=1
  aorow=2
  acrow=3
  aopeakrow=2
  oh=go.Ohlc(  
      x=_dates,
      open=_open_data,
      high=_high_data,
      low=_low_data,
      close=_close_data, 
      #color=df[signal_zcol_column_name],
      showlegend=False)
            # increasing_line_color=df[signal_zcol_column_name], decreasing_line_color=df[signal_zcol_column_name],

  _f4.add_trace(oh,row=mainrow,col=1)

  # Try to add some stuff when FDB
  #fig4.add_trace(go.Annotation('X',x=dates,
  #                            y=fdbb_data,row=1,col=1))
  gatorlinewidth=2
  # add Alligator
  _f4=addline2main(_f4,dfsrc[indicator_currentDegree_alligator_jaw_column_name],_dates,'Jaw','blue',gatorlinewidth,0.6,mainrow,1)
  _f4=addline2main(_f4,dfsrc[indicator_currentDegree_alligator_teeth_column_name],_dates,'Teeth',sellingZoneColor,gatorlinewidth,0.6,mainrow,1)
  _f4=addline2main(_f4,dfsrc[indicator_currentDegree_alligator_lips_column_name],_dates,'Lips',buyingZoneColor,gatorlinewidth,0.6,mainrow,1)


  # add Raptor (big Alligator
  _f4=addline2main(_f4,dfsrc[indicator_sixDegreeLarger_alligator_jaw_column_name],_dates,'BJaw','cyan',3,0.4,mainrow)
  _f4=addline2main(_f4,dfsrc[indicator_sixDegreeLarger_alligator_teeth_column_name],_dates,'BTeeth','magenta',3,0.4,mainrow)
  _f4=addline2main(_f4,dfsrc[indicator_sixDegreeLarger_alligator_lips_column_name],_dates,'BLips','yellow',3,0.4,mainrow)

  # fdbplot = go.Figure(data=[go.Scatter(
  #      x = df.index,
  #      y = df[signalBuy_fractalDivergentBar_column_name],
  #      mode = 'markers',)
  #  ])

  #fdbbpx= px.scatter(df,x='Date',y=signalBuy_fractalDivergentBar_column_name,color='aocolor')
  # fdbbpx= px.scatter(x=dates,y=fdbb_data)
  # fig4.add_trace(fdbbpx,row=1, col=1)
  #fig4.add_trace(go.Scatter(x=dates,y=fdbb_data),row=1, col=1)

  _f4.add_trace(go.Bar( 
                      x=_dates,
                      y=_ao_data,    
                      marker=dict(color=dfsrc['aocolor'].values.tolist(),
                      line=dict(color=dfsrc['aocolor'].values.tolist(), width=1)),
                      name='AO'), row=aorow, col=1)



  _f4.add_trace(go.Bar( 
                      x=_dates,
                      y=_ac_data,    
                      marker=dict(color=dfsrc['accolor'].values.tolist(),
                      line=dict(color=dfsrc['accolor'].values.tolist(), width=1)),
                      name='AC'), row=acrow, col=1)

  ############################## Ref to draw a Red or Green Zone
  # fig.add_shape(type="rect",
  #     x0=3, y0=1, x1=6, y1=2,
  #     line=dict(
  #         color="RoyalBlue",
  #         width=2,
  #     ),
  #     fillcolor="LightSkyBlue",
  # )

  ###################################### --@STCIssue How to ADd x0 and x1 ?
  # f4.add_shape(type="rect",
  #     x0=dtStart,y0.1.481987,x1=dtEnd, y1=1.3780,
  #     line=dict(
  #         color="RoyalBlue",
  #         width=2,
  #     ),
  #     fillcolor="LightSkyBlue",
  # )

  # ALL FDB PLOTTING using A SCATTER 
  _fdbplot =  go.Scatter(
      x = _dates_fdball,
      y = _fdball['High'],
      mode = 'markers',)

  _f4.add_trace(_fdbplot,row=1, col=1)
  # update layout by changing the plot size, hiding legends & rangeslider, and removing gaps between dates
  _f4.update_layout(height=_ch, width=_cw, 
                    showlegend=False, 
                    xaxis_rangeslider_visible=False)
  if useDTBreaks:
    _f4.update_xaxes(rangebreaks=[dict(values=_dt_breaks)])
  return _f4


# A 2x6 chart

# def pano_chart_pto221103(charts,_nbrows=3):
#   panocharts = sp.make_subplots(rows=_nbrows,cols=1,  row_heights=[110.1.4,110], shared_xaxes=True)
#   #column_widths=[75,75]
#   cl=1
#   r=1
#   for c in charts:
#     panocharts.add_trace(charts[c],row=r,col=cl)
#     r=r+1
#     # cl=cl+1
#     # if cl==3:
#     #   cl=1
#   return panocharts
  







def update(_f4,_ch,_cw,showlegent=False,xaxis_rangeslider_visible=False):
  _f4.update_layout(height=_ch, width=_cw, 
                    showlegend=False, 
                    xaxis_rangeslider_visible=False)
  
  
  













#%% Props and requests

from jgtpy import jgtconstants as c



def prepare_cds_for_ads_data(instrument, timeframe, nb_bar_on_chart, recreate_data=True):
    cache_data=False
    cache_dir = "cache"
    if cache_data:
        os.makedirs(cache_dir, exist_ok=True)

    fn =  instrument.replace("/", "-") + "_" + timeframe + ".csv"
    fnpath = os.path.join(cache_dir,fn)
    l.info("fnpath:"+ fnpath)

    #%% Load data
    l.info("-----------------  CDS  -----------------")
    if recreate_data:
        try:
            df = pds.getPH(instrument,timeframe,nb_bar_on_chart)
        except:
            l.warning("Could not get DF, trying to run thru WSL the update")
            wsl.jgtfxcli(instrument, timeframe, nb_bar_on_chart+35)
            df = pds.getPH(instrument,timeframe,nb_bar_on_chart)
        # Select the last 400 bars of the data
        try:
            selected = df.iloc[-nb_bar_on_chart-120:].copy()
        except:
            selected = df.copy()
            l.warning("Could not select the desired amount of bars, trying anyway with what we have")
            pass
        #print(selected)
        data = cds.createFromDF(selected)
        if cache_data:
            data.to_csv(fnpath)
    return data


def jgtxplot18c_231209(instrument,timeframe,nb_bar_on_chart = 375,recreate_data = True,show_plot=True):
    data = prepare_cds_for_ads_data(instrument, timeframe, nb_bar_on_chart, recreate_data)
    return plot_from_cds_df(data,instrument,timeframe,nb_bar_on_chart,show_plot)


def plot_from_pds_df(pdata,instrument,timeframe,nb_bar_on_chart = 375,show_plot=True):
  # Select the last 400 bars of the data
  try:
      selected = pdata.iloc[-nb_bar_on_chart-120:].copy()
  except:
      selected = pdata.copy()
      l.warning("Could not select the desired amount of bars, trying anyway with what we have")
      pass
  
  data = cds.createFromDF(selected)
  return plot_from_cds_df(data,instrument,timeframe,nb_bar_on_chart,show_plot)
  
  
def plot_from_cds_df(data,instrument,timeframe,nb_bar_on_chart = 375,show_plot=True):
  # Load dataset
  iprop = pds.get_instrument_properties(instrument)
  l.debug(iprop)
  pipsize = iprop["pipsize"]  # Access 'pipsize' using dictionary-like syntax
  l.debug(pipsize)
  #%% Read from file cache
  #data = pd.read_csv(fnpath)

  #%% Index stuff

  # Convert the index to datetime
  try:
      data.index = pd.to_datetime(data.index)
  except:
      l.error("Error converting index to datetime")
      pass


  #%% Data CONSTANTS

  main_plot_type="ohlc"

  _ao_coln = c.indicator_AO_awesomeOscillator_column_name
  _ac_coln = c.indicator_AC_accelerationDeceleration_column_name
  
  
  ao_upbar_color = "g"
  ao_dnbar_color = "r"
  ac_up_color = "darkgreen"
  ac_dn_color = "darkred"
  fdb_signal_buy_color = "g"
  fdb_signal_sell_color = "r"
  jaw_color = "blue"
  teeth_color = "red"
  lips_color = "green"
  fractal_up_color = "blue"
  fractal_dn_color = "blue"
  fractal_dn_color_higher = "blue"
  fractal_up_color_higher = "blue"
  ac_signal_buy_color = "lightgreen"
  ac_signal_sell_color = "yellow"

  fdb_marker_size = 7
  fractal_marker_size = 8
  ac_signals_marker_size = 24
  saucer_marker_size = 48
  fractal_degreehigher_marker_size = 20
  
  fdb_signal_marker = "o"
  fractal_up_marker="^"
  fractal_up_marker_higher= "^"
  fractal_dn_marker_higher = "v"
  fractal_dn_marker = "v"
  ac_signal_marker="o"

  #COLUMNS
  _jaw_coln = c.indicator_currentDegree_alligator_jaw_column_name
  _teeth_coln = c.indicator_currentDegree_alligator_teeth_column_name
  _lips_coln = c.indicator_currentDegree_alligator_lips_column_name

  _open_coln ="Open"
  _high_coln = "High"
  _low_coln = "Low"
  _close_coln = "Close"
  _barheight_coln = "bar_height"

  fh_col_dim = c.indicator_fractal_high_degree2_column_name
  fl_col_dim = c.indicator_fractal_low_degree2_column_name
  fh_col_dim_higher = c.indicator_fractal_high_degree8_column_name
  fl_col_dim_higher = c.indicator_fractal_low_degree8_column_name


  _fdb_coln = c.signalCode_fractalDivergentBar_column_name
  _fdbb_coln = c.signalBuy_fractalDivergentBar_column_name
  _fdbs_coln = c.signalSell_fractalDivergentBar_column_name


  _acb_coln = c.signalBuy_AC_acceleration_column_name  
  _acs_coln = c.signalSell_AC_deceleration_column_name

  #plot config
  main_plot_panel_id=0
  ao_plot_panel_id=1
  ac_plot_panel_id=2

  plot_style = "yahoo"
  fig_ratio_x = 24
  fig_ratio_y = 10
  
  #%% Select the last 400 bars of the data

  # Select the last 400 bars of the data
  try:
      data_last_selection = data.iloc[-nb_bar_on_chart:].copy()
  except:
      l.warning("Could not select the desired amount of bars, trying anyway with what we have")
      pass

  # Make OHLC bars plot
  ohlc = data_last_selection[[_open_coln, _high_coln, _low_coln, _close_coln]]





  #%% AO/AC
  # AO / AC
  # Calculate the color for 'ao' and 'ac' bar
  colors_ao = [
      ao_upbar_color if (data_last_selection[_ao_coln][i] - data_last_selection[_ao_coln][i - 1] > 0) else ao_dnbar_color
      for i in range(1, len(data_last_selection[_ao_coln]))
  ]
  colors_ao.insert(0, ao_dnbar_color)

  colors_ac = [
      ac_up_color
      if (data_last_selection[_ac_coln][i] - data_last_selection[_ac_coln][i - 1] > 0)
      else ac_dn_color
      for i in range(1, len(data_last_selection[_ac_coln]))
  ]
  colors_ac.insert(0, ac_dn_color)
  # Make 'ao' and 'ac' oscillator plot
  ao_plot = mpf.make_addplot(
      data_last_selection[_ao_coln], panel=ao_plot_panel_id, color=colors_ao, secondary_y=False, type="bar"
  )
  ac_plot = mpf.make_addplot(
      data_last_selection[_ac_coln], panel=ac_plot_panel_id, color=colors_ac, secondary_y=False, type="bar"
  )
  # @STCGoal Make AO/AC signals plotted



  #%% Alligator

  #@STCIssue no offset data in, not offset columns: jaws_tmp,teeth_tmp,lips_tmp

  # Make Alligator's lines plot

  jaw_plot = mpf.make_addplot(data_last_selection[_jaw_coln], panel=main_plot_panel_id, color=jaw_color)
  teeth_plot = mpf.make_addplot(data_last_selection[_teeth_coln], panel=main_plot_panel_id, color=teeth_color)
  lips_plot = mpf.make_addplot(data_last_selection[_lips_coln], panel=main_plot_panel_id, color=lips_color)


  #%% Offsets and various values
  # offset

  min_timeframe = getMinByTF(timeframe)
  price_mean = data_last_selection[_close_coln].mean()

  # Calculate the bar height for each row
  data_last_selection[_barheight_coln] = data_last_selection[_high_coln] - data_last_selection[_low_coln]


  # Calculate the average bar height
  average_bar_height = data_last_selection[_barheight_coln].mean()
  low_min = data_last_selection[_low_coln].min()
  high_max = data_last_selection[_high_coln].max()
  ao_max = data_last_selection[_ao_coln].max()
  ao_min = data_last_selection[_ao_coln].min()
  ac_max = data_last_selection[_ac_coln].max()
  ac_min = data_last_selection[_ac_coln].min()


  #%% FDB

  # Align fdbb with OHLC bars if value is '1.0'
  data_last_selection.loc[:,_fdbb_coln] = np.where(
      data_last_selection[_fdb_coln] == 1.0, data_last_selection[_high_coln], np.nan
  )
  data_last_selection.loc[:,_fdbs_coln] = np.where(
      data_last_selection[_fdb_coln] == -1.0, data_last_selection[_low_coln], np.nan
  )

  # Date,Volume,Open,High,Low,Close,Median,ac,jaw,teeth,lips,bjaw,bteeth,blips,ao,fh,fl,fh3,fl3,fh5,fl5,fh8,fl8,fh13,fl13,fh21,fl21,fh34,fl34,fh55,fl55,fh89,fl89,fdbb,fdbs,fdb,aof,aoaz,aobz,zlc,zlcb,zlcs,zcol,sz,bz,acs,acb,ss,sb



  #%% Saucer
  _saucer_b_coln = c.signalBuy_saucer_column_name
  _saucer_s_coln = c.signalSell_saucer_column_name

  # Saucer
  # Align saucer with AO bars if value is '1.0'
  data_last_selection.loc[:,_saucer_b_coln] = np.where(data_last_selection[_saucer_b_coln] == 1.0, ao_max, np.nan)
  data_last_selection.loc[:,_saucer_s_coln] = np.where(data_last_selection[_saucer_s_coln] == 1.0, ao_min, np.nan)

  saucer_offset_value = 0
  
  # Make Buy Signal plot
  sb_plot = mpf.make_addplot(
      data_last_selection[_saucer_b_coln] + saucer_offset_value,
      panel=ao_plot_panel_id,
      type="scatter",
      markersize=saucer_marker_size,
      marker="|",
      color="g",
  )
  
  # Make Sell Signal plot
  ss_plot = mpf.make_addplot(
      data_last_selection[_saucer_s_coln] - saucer_offset_value,
      panel=ao_plot_panel_id,
      type="scatter",
      markersize=saucer_marker_size,
      marker="|",
      color="r",
  )

  #%% Outputs checks
  l.debug("---------------------------------------")
  l.debug("AC Min/Max: " + str(ac_min) + "/" + str(ac_max))
  l.debug("---------------------------------------")


  #%% AC Signal


  # Align saucer with OHLC bars if value is '1.0'
  data_last_selection.loc[:,_acb_coln] = np.where(
      data_last_selection[_acb_coln] == 1.0, data_last_selection[_ac_coln], np.nan
  )
  data_last_selection.loc[:,_acs_coln] = np.where(
      data_last_selection[_acs_coln] == 1.0, data_last_selection[_ac_coln], np.nan
  )

  sig_ac_offset_value = 0


  # Make Buy Signal plot
  acb_plot = mpf.make_addplot(
      data_last_selection[_acb_coln] + sig_ac_offset_value,
      panel=ac_plot_panel_id,
      type="scatter",
      markersize=ac_signals_marker_size,
      marker=ac_signal_marker,
      color=ac_signal_buy_color,
  )
  # Make Sell Signal plot
  acs_plot = mpf.make_addplot(
      data_last_selection[_acs_coln] - sig_ac_offset_value,
      panel=ac_plot_panel_id,
      type="scatter",
      markersize=ac_signals_marker_size,
      marker=ac_signal_marker,
      color=ac_signal_sell_color,
  )


  #%% Print the summary statistics of the 'ac' column
  l.debug("Summary Stats:")
  l.debug(data_last_selection[_ac_coln].describe())



  #%% Make FDB plot


  fdb_tick_offset = average_bar_height  # pipsize * 111
  fdb_offset_value = average_bar_height / 2  # pipsize * fdb_tick_offset

  fdbb_up_plot, fdbs_down_plot = make_plot__fdb_signals(fdb_signal_buy_color, fdb_signal_sell_color, fdb_marker_size, fdb_signal_marker, _fdbb_coln, _fdbs_coln, main_plot_panel_id, data_last_selection, fdb_offset_value)


  #%% Make Fractals plot


  fractal_offset_value = average_bar_height / 2  # pipsize * fractal_tick_offset

  fractal_tick_offset = pipsize * 111  # price_mean*10

  # Align fractals with OHLC bars


  data_last_selection.loc[:,fh_col_dim] = np.where(
      (data_last_selection[_high_coln] > data_last_selection[_teeth_coln])
      & (data_last_selection[fh_col_dim] == True),
      data_last_selection[_high_coln],
      np.nan,
  )


  data_last_selection.loc[:,fl_col_dim] = np.where(
      (data_last_selection[_low_coln] < data_last_selection[_teeth_coln])
      & (data_last_selection[fl_col_dim] == True),
      data_last_selection[_low_coln] - fractal_offset_value,
      np.nan,
  )





  fractal_up_plot, fractal_down_plot = make_plot__fractals_indicator(fractal_up_color, fractal_dn_color, fractal_marker_size, fractal_up_marker, fractal_dn_marker, fh_col_dim, fl_col_dim, main_plot_panel_id, data_last_selection, fractal_offset_value)

  #%% Fractal higher dim


  data_last_selection.loc[:,fh_col_dim_higher] = np.where(
      (data_last_selection[_high_coln] > data_last_selection[_teeth_coln])
      & (data_last_selection[fh_col_dim_higher] == True),
      data_last_selection[_high_coln],
      np.nan,
  )


  data_last_selection.loc[:,fl_col_dim_higher] = np.where(
      (data_last_selection[_low_coln] < data_last_selection[_teeth_coln])
      & (data_last_selection[fl_col_dim_higher] == True),
      data_last_selection[_low_coln] - fractal_offset_value,
      np.nan,
  )


  #%% PLot higher fractal


  fractal_up_plot_higher, fractal_down_plot_higher = make_plot_fractals_degreehigher_indicator(fractal_dn_color_higher, fractal_up_color_higher, fractal_degreehigher_marker_size, fractal_up_marker_higher, fractal_dn_marker_higher, fh_col_dim_higher, fl_col_dim_higher, main_plot_panel_id, data_last_selection, fractal_offset_value)





  #%% Print Mean
  #l.debug("Mean: " + (price_mean).astype(str))


  #%% Plotting
  addplot = [
      jaw_plot,
      teeth_plot,
      lips_plot,
      fractal_up_plot,
      fractal_down_plot,
      fractal_up_plot_higher,
      fractal_down_plot_higher,
      fdbb_up_plot,
      fdbs_down_plot,
      sb_plot,
      ss_plot,
      ao_plot,
      ac_plot,
      acs_plot,
      acb_plot,
  ]

  # Filter out empty plots
  #addplot = [plot for plot in addplot if plot['data'].size > 0]

  fig, axes = mpf.plot(
      ohlc,
      type=main_plot_type,
      style=plot_style,
      addplot=addplot,
      volume=False,
      figratio=(fig_ratio_x, fig_ratio_y),
      title=instrument + "  " + timeframe,
      returnfig=True,
      tight_layout=True,
  )

  # fig, axes = mpf.plot(
  #     ohlc,
  #     type=main_plot_type,
  #     style=plot_style,
  #     addplot=[
  #         jaw_plot,
  #         teeth_plot,
  #         lips_plot,
  #         fractal_up_plot,
  #         fractal_down_plot,
  #         fractal_up_plot_higher,
  #         fractal_down_plot_higher,
  #         fdbb_up_plot,
  #         fdbs_down_plot,
  #         sb_plot,
  #         ss_plot,
  #         ao_plot,
  #         ac_plot,
  #         acs_plot,
  #         acb_plot,
  #     ],
  #     volume=False,
  #     figratio=(fig_ratio_x, fig_ratio_y),
  #     title=instrument + "  " + timeframe,
  #     returnfig=True,
  #     tight_layout=True,
  # )

  # Set y-axis limits
  axes[main_plot_panel_id].set_ylim(
      low_min - fdb_offset_value - pipsize * 20,
      high_max + fdb_offset_value + pipsize * 20,
  )

  # Get current x-axis limits
  x_min, x_max = axes[main_plot_panel_id].get_xlim()

  axe2ymin, axe2ymax = axes[ac_plot_panel_id].get_ylim()
  l.debug("axe2ymin: " + str(axe2ymin))
  l.debug("axe2ymax: " + str(axe2ymax))

  # Calculate new x-axis limit
  new_x_max = x_max + 8  # Add 8 for future bars

  # Set new x-axis limit
  axes[main_plot_panel_id].set_xlim(x_min, new_x_max)


  # Align the title to the left
  fig.suptitle(instrument + "  " + timeframe, x=0.05, ha="left")

  # Set the font size of the x-axis labels
  for ax in axes:
      ax.tick_params(axis="x", labelsize=6)

  # Set the font size of the Date column
  axes[main_plot_panel_id].tick_params(axis="x", labelsize=6)

  if show_plot:
      plt.show()
  return fig,axes

def make_plot_fractals_degreehigher_indicator(fractal_dn_color_higher, fractal_up_color_higher, fractal_degreehigher_marker_size, fractal_up_marker_higher, fractal_dn_marker_higher, fh_col_dim_higher, fl_col_dim_higher, main_plot_panel_id, data_last_selection, fractal_offset_value):
    fractal_up_plot_higher = mpf.make_addplot(
      data_last_selection[fh_col_dim_higher] + fractal_offset_value,
      panel=main_plot_panel_id,
      type="scatter",
      markersize=fractal_degreehigher_marker_size,
      marker=fractal_up_marker_higher,
      color=fractal_up_color_higher,
  )
    fractal_down_plot_higher = mpf.make_addplot(
      data_last_selection[fl_col_dim_higher],
      panel=main_plot_panel_id,
      type="scatter",
      markersize=fractal_degreehigher_marker_size,
      marker=fractal_dn_marker_higher,
      color=fractal_dn_color_higher,
  )
    
    return fractal_up_plot_higher,fractal_down_plot_higher

def make_plot__fractals_indicator(fractal_up_color, fractal_dn_color, fractal_marker_size, fractal_up_marker, fractal_dn_marker, fh_col_dim, fl_col_dim, main_plot_panel_id, data_last_selection, fractal_offset_value):
    fractal_up_plot = mpf.make_addplot(
      data_last_selection[fh_col_dim] + fractal_offset_value,
      panel=main_plot_panel_id,
      type="scatter",
      markersize=fractal_marker_size,
      marker=fractal_up_marker,
      color=fractal_up_color,
  )
    fractal_down_plot = mpf.make_addplot(
      data_last_selection[fl_col_dim],
      panel=main_plot_panel_id,
      type="scatter",
      markersize=fractal_marker_size,
      marker=fractal_dn_marker,
      color=fractal_dn_color,
  )
    
    return fractal_up_plot,fractal_down_plot


def make_plot__fdb_signals(fdb_signal_buy_color, fdb_signal_sell_color, fdb_marker_size, fdb_signal_marker, fdbb_coln, fdbs_coln, main_plot_panel_id, data_last_selection, fdb_offset_value):
        """
        Creates scatter plots for FDB buy and sell signals based on the given parameters.

        Args:
                fdb_signal_buy_color (str): Color of the scatter plot for buy signals.
                fdb_signal_sell_color (str): Color of the scatter plot for sell signals.
                fdb_marker_size (int): Size of the markers in the scatter plot.
                fdb_signal_marker (str): Marker style for the scatter plot.
                fdbb_coln (str): Column name for buy signals in the data.
                fdbs_coln (str): Column name for sell signals in the data.
                main_plot_panel_id (int): ID of the main plot panel.
                data_last_selection (pandas.DataFrame): Data containing the buy and sell signals.
                fdb_offset_value (float): Offset value to adjust the scatter plot positions.

        Returns:
                tuple: A tuple containing the scatter plot for buy signals and the scatter plot for sell signals.
        """
        
        fdbb_up_plot = make_plot_fdbb_signal(fdb_signal_buy_color, fdb_marker_size, fdb_signal_marker, fdbb_coln, main_plot_panel_id, data_last_selection, fdb_offset_value)

        fdbs_down_plot = make_plot_fdbs_signal(fdb_signal_sell_color, fdb_marker_size, fdb_signal_marker, fdbs_coln, main_plot_panel_id, data_last_selection, fdb_offset_value)
        
        return fdbb_up_plot,fdbs_down_plot

def make_plot_fdbs_signal(fdb_signal_sell_color, fdb_marker_size, fdb_signal_marker, fdbs_coln, main_plot_panel_id, data_last_selection, fdb_offset_value):
    fdbs_down_plot = mpf.make_addplot(
            data_last_selection[fdbs_coln] - fdb_offset_value,
            panel=main_plot_panel_id,
            type="scatter",
            markersize=fdb_marker_size,
            marker=fdb_signal_marker,
            color=fdb_signal_sell_color,
    )

    return fdbs_down_plot

def make_plot_fdbb_signal(fdb_signal_buy_color, fdb_marker_size, fdb_signal_marker, fdbb_coln, main_plot_panel_id, data_last_selection, fdb_offset_value):
    fdbb_up_plot = mpf.make_addplot(
            data_last_selection[fdbb_coln] + fdb_offset_value,
            panel=main_plot_panel_id,
            type="scatter",
            markersize=fdb_marker_size,
            marker=fdb_signal_marker,
            color=fdb_signal_buy_color,
    )

    return fdbb_up_plot
  #return plt


# %% ALias function (future name)

def plotcdf(data,instrument, timeframe, nb_bar_on_chart=375,show_plot=True):
  return plot_from_cds_df(data,instrument,timeframe,nb_bar_on_chart,show_plot)

def plot(instrument, timeframe, nb_bar_on_chart=375, recreate_data=True, show_plot=True):
    """
    Plot the chart for a given instrument and timeframe.

    Parameters:
    instrument (str): The name of the instrument.
    timeframe (str): The timeframe for the chart.
    nb_bar_on_chart (int, optional): The number of bars to display on the chart. Default is 375.
    recreate_data (bool, optional): Whether to recreate the data for the chart. Default is True.
    show_plot (bool, optional): Whether to display the plot. Default is True.

    Returns:
    fig: The figure object of the plot.
    axes: The axes object of the plot.
    """
    fig, axes = jgtxplot18c_231209(instrument, timeframe, nb_bar_on_chart, recreate_data, show_plot)
    return fig, axes

  




