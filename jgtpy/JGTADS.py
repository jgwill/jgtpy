#@title ADS

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



#%% Props and requests

import adshelper as ah
from jgtpy import jgtconstants as c




def jgtxplot18c_231209(instrument,timeframe,nb_bar_on_chart = 375,recreate_data = True,show_plot=True):
    data = ah.prepare_cds_for_ads_data(instrument, timeframe, nb_bar_on_chart, recreate_data)
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
  
  
def plot_from_cds_df(data,instrument,timeframe,nb_bar_on_chart = 375,show_plot=True,plot_ao_peaks=False):
  # Load dataset
  iprop = pds.get_instrument_properties(instrument)
  l.debug(iprop)
  pipsize = iprop["pipsize"]  # Access 'pipsize' using dictionary-like syntax
  l.debug(pipsize)

  # Convert the index to datetime
  try:
      data.index = pd.to_datetime(data.index)
  except:
      l.error("Error converting index to datetime")
      pass



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

  _open_coln = c.open_column_name
  _high_coln = c.high_column_name
  _low_coln = c.low_column_name
  _close_coln = c.close_column_name
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
      data_last_selection = data
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

  

  #%% ao_peak_above Plot
  if plot_ao_peaks:
    ao_peaks_marker_size = 42
        #%% AO Peaks
    ao_peak_bellow_coln = 'ao_peak_bellow'
    ao_peak_above_coln = 'ao_peak_above'
    
    # AO Peaks
    # Align AO Peaks with AO bars if value is '1.0'
    data_last_selection.loc[:,ao_peak_bellow_coln] = np.where(data_last_selection[ao_peak_bellow_coln] == 1.0, ao_max/2, np.nan)
    data_last_selection.loc[:,ao_peak_above_coln] = np.where(data_last_selection[ao_peak_above_coln] == 1.0, ao_min/2, np.nan)
    
    ao_peak_offset_value = 0
    ao_peak_above_marker_higher= "^"
    ao_peak_bellow__marker_higher = "v"
    
    # Make AO Peak Bellow plot
    aopbellow_plot = mpf.make_addplot(
        data_last_selection[ao_peak_bellow_coln] +ao_peak_offset_value,
        panel=ao_plot_panel_id,
        type="scatter",
        markersize=ao_peaks_marker_size,
        marker=ao_peak_bellow__marker_higher,
        color="r",
    )
    
    # Make AO Peak Above plot
    aopabove_plot = mpf.make_addplot(
        data_last_selection[ao_peak_above_coln] -ao_peak_offset_value,
        panel=ao_plot_panel_id,
        type="scatter",
        markersize=ao_peaks_marker_size,
        marker=ao_peak_above_marker_higher,
        color="g",
    )
    
    

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
  
  
  
  
  if plot_ao_peaks:
      addplot.append(aopabove_plot)
      addplot.append(aopbellow_plot)


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

  




