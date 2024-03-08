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
from jgtutils import jgtwslhelper as wsl

#@STCGoal Unified JGTChartConfig & JGTADSRequest
from JGTChartConfig import JGTChartConfig
from JGTADSRequest import JGTADSRequest

import adshelper as ah
from jgtutils import jgtconstants as c

AO = c.AO
AC = c.AC

warnings.filterwarnings("ignore", category=FutureWarning)

import os

#import kaleido
# import plotly

import JGTConfig as jgtc


# import plotly.graph_objects as go
# import plotly.subplots as sp



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

def plot_from_cds_df__DEBUG(df,instrument:str,timeframe:str,show:bool=True,plot_ao_peaks:bool=True,cc: JGTChartConfig=None,crop_last_dt:str=None):
    data = ah.prepare_cds_for_ads_data(instrument, timeframe,cc=cc,crop_last_dt=crop_last_dt) #@STCGoal  Same Prep as if reading and setting it
    return None




def jgtxplot18c_231209(instrument:str,timeframe:str,show:bool=True,plot_ao_peaks:bool=True,cc: JGTChartConfig=None,tlid_range:str=None,crop_last_dt:str=None,use_fresh=False,rq:JGTADSRequest=None):
      
    data = ah.prepare_cds_for_ads_data(instrument, timeframe,tlid_range=tlid_range,cc=cc,crop_last_dt=crop_last_dt,use_fresh=use_fresh,rq=rq) #@STCGoal Supports TLID
    #@STCIssue Desired Number of Bars ALREADY SELECTED IN THERE
    #print(len(data))
    #data.to_csv("debug_data" + instrument.replace("/","-") + timeframe + ".csv")
    try:
        return plot_from_cds_df(data,instrument,timeframe,show=show,plot_ao_peaks=plot_ao_peaks,cc=cc)
    except:
        print("ERROR - Returning ALT Plotting (" + instrument + " " + timeframe + ")")
        return plot_from_cds_df_ALT(data,instrument,timeframe,show=show,plot_ao_peaks=plot_ao_peaks,cc=cc)


def plot_from_pds_df(pdata,instrument:str,timeframe:str,show:int=True,plot_ao_peaks=True,cc: JGTChartConfig=None,tlid_range:str=None):
    if cc is None:
        cc= JGTChartConfig()
    
    cds_required_amount_of_bar_for_calc = cc.cds_required_amount_of_bar_for_calc
    nb_bar_on_chart = cc.nb_bar_on_chart

    # Select the last cds_required_amount_of_bar_for_calc
    #@STCIssue Desired Number of Bars MUST SUPPORT TLID RANGE
    try:
        selected = pdata.iloc[-nb_bar_on_chart-cds_required_amount_of_bar_for_calc:].copy() #@STCGoal A Unified way to select the data
    except:
        selected = pdata.copy()
        l.warning("Could not select the desired amount of bars, trying anyway with what we have")
        pass

    data1 = cds.createFromDF(selected)

    #@STCGoal Make sure we have the amount of bars we were requested (and not more)
    try: 
        data=data1.iloc[-nb_bar_on_chart:].copy()
    except:
        data = data1.copy()
        l.warning("Could not select the desired amount of bars, trying anyway with what we have")
        pass
    return plot_from_cds_df(data,instrument,timeframe,show=show,plot_ao_peaks=plot_ao_peaks)



def plot_from_cds_df(data:pd.DataFrame,instrument:str,timeframe:str,show=True,plot_ao_peaks:bool=True,cc: JGTChartConfig=None):
    
    """
    Plot OHLC bars, indicators, and signals from a pandas DataFrame.

    Args:
        data (pandas.DataFrame): The input DataFrame containing OHLC data.
        instrument (str): The instrument symbol.
        timeframe (str): The timeframe of the data.
        show (bool, optional): Whether to display the plot. Defaults to True.
        plot_ao_peaks (bool, optional): Whether to plot AO peaks. Defaults to False.
        cc (JGTChartConfig, optional): The chart configuration object. Defaults to None.

    Returns:
        fig: The figure object of the plot.
        axes: The axes object of the plot.
    """
    if cc is None:
        cc= JGTChartConfig()
   
    
    nb_bar_on_chart = cc.nb_bar_on_chart
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
    
        
    
    fig_ratio_x = cc.fig_ratio_x
    fig_ratio_y = cc.fig_ratio_y
    
    fdb_signal_buy_color = cc.fdb_signal_buy_color
    fdb_signal_sell_color = cc.fdb_signal_sell_color
    jaw_color = cc.jaw_color
    teeth_color = cc.teeth_color
    lips_color = cc.lips_color
    fractal_up_color = cc.fractal_up_color
    fractal_dn_color = cc.fractal_dn_color
    fractal_dn_color_higher = cc.fractal_dn_color_higher
    fractal_up_color_higher = cc.fractal_up_color_higher
    ac_signal_buy_color = cc.ac_signal_buy_color
    ac_signal_sell_color = cc.ac_signal_sell_color
    fdb_marker_size = cc.fdb_marker_size
    fractal_marker_size = cc.fractal_marker_size
    saucer_marker_size = cc.saucer_marker_size
    fractal_degreehigher_marker_size = cc.fractal_degreehigher_marker_size
    fdb_signal_marker = cc.fdb_signal_marker
    fractal_up_marker = cc.fractal_up_marker
    fractal_up_marker_higher = cc.fractal_up_marker_higher
    fractal_dn_marker_higher = cc.fractal_dn_marker_higher
    fractal_dn_marker = cc.fractal_dn_marker
    plot_style = cc.plot_style
    saucer_buy_color = cc.saucer_buy_color
    saucer_sell_color = cc.saucer_sell_color
    saucer_marker = cc.saucer_marker
    price_peak_bellow_marker = cc.price_peak_bellow_marker
    price_peak_above_marker = cc.price_peak_above_marker
    price_peak_marker_size = cc.price_peak_marker_size
    price_peak_above_color = cc.price_peak_above_color
    price_peak_bellow_color = cc.price_peak_bellow_color
    
    ac_signals_marker_size = cc.ac_signals_marker_size
    ac_signal_marker = cc.ac_signal_marker
    
    acb_plot_type =  cc.acb_plot_type
    
    ao_peaks_marker_size = cc.ao_peaks_marker_size
    ao_peak_offset_value = cc.ao_peak_offset_value
    ao_peak_above_marker_higher = cc.ao_peak_above_marker_higher
    ao_peak_bellow__marker_higher = cc.ao_peak_bellow__marker_higher
    aop_bellow_color = cc.aop_bellow_color
    aop_above_color = cc.aop_above_color
    
    #COLUMNS
    JAW = c.JAW
    TEETH = c.TEETH
    LIPS = c.LIPS
    
    OPEN = c.OPEN
    HIGH = c.HIGH
    LOW = c.LOW
    CLOSE = c.CLOSE
    BAR_HEIGHT = c.BAR_HEIGHT #"bar_height"
    
    FH = c.FH
    FL = c.FL
    FHH = c.FH8
    FLH = c.FL8
    
    
    FDB = c.FDB
    FDBB = c.FDBB
    FDBS = c.FDBS
    
    
    ACB = c.ACB  
    ACS = c.ACS
    
    #plot config
    main_plot_panel_id=cc.main_plot_panel_id
    ao_plot_panel_id=cc.ao_plot_panel_id
    ac_plot_panel_id=cc.ac_plot_panel_id
    
    
    
    #%% Select the last 400 bars of the data
    
    data_last_selection = data
    # Select the last 400 bars of the data
    tst_len_data = len(data)
    if nb_bar_on_chart != tst_len_data:    
        data_last_selection = _select_charting_nb_bar_on_chart(data, nb_bar_on_chart)
    l_datasel = len(data_last_selection)
    
    # Make OHLC bars plot
    ohlc = data_last_selection[[OPEN, HIGH, LOW, CLOSE]]
    
    
    
    
    
    #%% AO/AC
    # AO / AC Plotting
    ao_plot,ac_plot = make_plot__ao_ac(data_last_selection,cc,ao_plot_panel_id,ac_plot_panel_id)
    
    
    # @STCGoal Make AO/AC signals plotted
    
    
    
    #%% Alligator
    
    #@STCIssue no offset data in, not offset columns: jaws_tmp,teeth_tmp,lips_tmp
    
    # Make Alligator's lines plot
    
    jaw_plot, teeth_plot, lips_plot = _make_alligator_line_plots(jaw_color, teeth_color, lips_color, JAW, TEETH, LIPS, main_plot_panel_id, data_last_selection)
    
    
    #%% Offsets and various values
    # offset
    
    #min_timeframe = getMinByTF(timeframe)
    #price_mean = data_last_selection[CLOSE].mean()
    
    # Calculate the bar height for each row
    data_last_selection[BAR_HEIGHT] = data_last_selection[HIGH] - data_last_selection[LOW]
    
    
    # Calculate the average bar height
    average_bar_height = data_last_selection[BAR_HEIGHT].mean()
    #low_min = data_last_selection[LOW].min()
    #high_max = data_last_selection[HIGH].max()
    ao_max = data_last_selection[AO].max()
    ao_min = data_last_selection[AO].min()
    ac_max = data_last_selection[AC].max()
    ac_min = data_last_selection[AC].min()
    
    
    #%% FDB
    
    
    # Align fdbb with OHLC bars if value is '1.0'
    data_last_selection.loc[:,FDBB] = np.where(
        data_last_selection[FDB] == 1.0, data_last_selection[HIGH], np.nan
    )
    data_last_selection.loc[:,FDBS] = np.where(
        data_last_selection[FDB] == -1.0, data_last_selection[LOW], np.nan
    )
    
    
    # Date,Volume,Open,High,Low,Close,Median,ac,jaw,teeth,lips,bjaw,bteeth,blips,ao,fh,fl,fh3,fl3,fh5,fl5,fh8,fl8,fh13,fl13,fh21,fl21,fh34,fl34,fh55,fl55,fh89,fl89,fdbb,fdbs,fdb,aof,aoaz,aobz,zlc,zlcb,zlcs,zcol,sz,bz,acs,acb,ss,sb
    
    
    #%% ao_peak_above Plot
    if plot_ao_peaks:
            #%% AO Peaks
        AO_PEAK_BELLOW = c.AO_PEAK_BELLOW #'ao_peak_bellow'
        AO_PEAK_ABOVE = c.AO_PEAK_ABOVE #'ao_peak_above'
        
        # AO Peaks
        # Align AO Peaks with AO bars if value is '1.0'
        data_last_selection.loc[:,AO_PEAK_BELLOW] = np.where(data_last_selection[AO_PEAK_BELLOW] == 1.0, ao_max/1.5, np.nan)
        data_last_selection.loc[:,AO_PEAK_ABOVE] = np.where(data_last_selection[AO_PEAK_ABOVE] == 1.0, ao_min/1.5, np.nan)
        
        
        # Make AO Peak Bellow plot

        aopbellow_plot = mpf.make_addplot(
            data_last_selection[AO_PEAK_BELLOW] +ao_peak_offset_value,
            panel=ao_plot_panel_id,
            type="scatter",
            markersize=ao_peaks_marker_size,
            marker=ao_peak_bellow__marker_higher,
            color=aop_bellow_color,
        )
        
        # Make AO Peak Above plot
        aopabove_plot = mpf.make_addplot(
            data_last_selection[AO_PEAK_ABOVE] -ao_peak_offset_value,
            panel=ao_plot_panel_id,
            type="scatter",
            markersize=ao_peaks_marker_size,
            marker=ao_peak_above_marker_higher,
            color=aop_above_color,
        )
        
        
        
        price_peak_offset_value=average_bar_height / 3 * 5
        
        PRICE_PEAK_ABOVE = c.PRICE_PEAK_ABOVE #'price_peak_above'
        PRICE_PEAK_BELLOW = c.PRICE_PEAK_BELLOW #'price_peak_bellow'
        
        
        data_last_selection.loc[:,PRICE_PEAK_ABOVE] = np.where(
            data_last_selection[PRICE_PEAK_ABOVE] == 1.0, data_last_selection[HIGH], np.nan
        )
        data_last_selection.loc[:,PRICE_PEAK_BELLOW] = np.where(
            data_last_selection[PRICE_PEAK_BELLOW] == 1.0, data_last_selection[LOW], np.nan
        )
        
        price_peak_above_plot, price_peak_bellow_plot = make_plot__price_peaks__indicator(price_peak_above_color, price_peak_bellow_color, price_peak_marker_size, price_peak_above_marker, price_peak_bellow_marker, PRICE_PEAK_ABOVE, PRICE_PEAK_BELLOW, main_plot_panel_id, data_last_selection, price_peak_offset_value)
        
        
        
    #%% Saucer
    SB = c.SB
    SS = c.SS
    
    # Saucer
    # Align saucer with AO bars if value is '1.0'
    data_last_selection.loc[:,SB] = np.where(data_last_selection[SB] == 1.0, ao_max, np.nan)
    data_last_selection.loc[:,SS] = np.where(data_last_selection[SS] == 1.0, ao_min, np.nan)
    
    saucer_offset_value = 0
    

    # Make Buy Signal plot

    sb_plot = mpf.make_addplot(
        data_last_selection[SB] + saucer_offset_value,
        panel=ao_plot_panel_id,
        type="scatter",
        markersize=saucer_marker_size,
        marker=saucer_marker,
        color=saucer_buy_color,
    )
    
    
    # Make Sell Signal plot
    ss_plot = mpf.make_addplot(
        data_last_selection[SS] - saucer_offset_value,
        panel=ao_plot_panel_id,
        type="scatter",
        markersize=saucer_marker_size,
        marker=saucer_marker,
        color=saucer_sell_color,
    )
    
    
    #%% Outputs checks
    l.debug("---------------------------------------")
    l.debug("AC Min/Max: " + str(ac_min) + "/" + str(ac_max))
    l.debug("---------------------------------------")
    
    
    #%% AC Signal
    
    sig_ac_offset_value = 0
    
    
    # Align ACB with OHLC bars if value is '1.0'
    data_last_selection.loc[:,ACB] = np.where(
        data_last_selection[ACB] == 1.0, data_last_selection[AC], np.nan
    )
    data_last_selection.loc[:,ACS] = np.where(
        data_last_selection[ACS] == 1.0, data_last_selection[AC], np.nan
    )



    # Make Buy Signal plot
    acb_plot = mpf.make_addplot(
        data_last_selection[ACB] + sig_ac_offset_value,
        panel=ac_plot_panel_id,
        type=acb_plot_type,
        markersize=ac_signals_marker_size,
        marker=ac_signal_marker,
        color=ac_signal_buy_color,
    )
    # Make Sell Signal plot
    acs_plot = mpf.make_addplot(
        data_last_selection[ACS] - sig_ac_offset_value,
        panel=ac_plot_panel_id,
        type=acb_plot_type,
        markersize=ac_signals_marker_size,
        marker=ac_signal_marker,
        color=ac_signal_sell_color,
    )


    #%% Print the summary statistics of the 'ac' column
    l.debug("Summary Stats:")
    l.debug(data_last_selection[AC].describe())



    #%% Make FDB plot


    fdb_tick_offset = average_bar_height  # pipsize * 111
    fdb_offset_value = average_bar_height / 2  # pipsize * fdb_tick_offset

    fdbb_up_plot, fdbs_down_plot = make_plot__fdb_signals(fdb_signal_buy_color, fdb_signal_sell_color, fdb_marker_size, fdb_signal_marker, FDBB, FDBS, main_plot_panel_id, data_last_selection, fdb_offset_value)


    #%% Make Fractals plot


    fractal_offset_value = average_bar_height / 2  # pipsize * fractal_tick_offset

    fractal_tick_offset = pipsize * 111  # price_mean*10

    # Align fractals with OHLC bars


    data_last_selection.loc[:,FH] = np.where(
        (data_last_selection[HIGH] > data_last_selection[TEETH])
        & (data_last_selection[FH] == True),
        data_last_selection[HIGH],
        np.nan,
    )


    data_last_selection.loc[:,FL] = np.where(
        (data_last_selection[LOW] < data_last_selection[TEETH])
        & (data_last_selection[FL] == True),
        data_last_selection[LOW] - fractal_offset_value,
        np.nan,
    )


    fractal_up_plot, fractal_down_plot = make_plot__fractals_indicator(fractal_up_color, fractal_dn_color, fractal_marker_size, fractal_up_marker, fractal_dn_marker, FH, FL, main_plot_panel_id, data_last_selection, fractal_offset_value)




    #%% Fractal higher dim
    #@STCIssue The Data IS not Prepared in the PLot Maker.  Is this a problem? Should it be? Should it be done here or into a  function preparing the data for the plot? That way we could use it for more plot Types.


    data_last_selection.loc[:,FHH] = np.where(
        (data_last_selection[HIGH] > data_last_selection[TEETH])
        & (data_last_selection[FHH] == True),
        data_last_selection[HIGH],
        np.nan,
    )


    data_last_selection.loc[:,FLH] = np.where(
        (data_last_selection[LOW] < data_last_selection[TEETH])
        & (data_last_selection[FLH] == True),
        data_last_selection[LOW] - fractal_offset_value,
        np.nan,
    )


    #%% PLot higher fractal


    fractal_up_plot_higher, fractal_down_plot_higher = make_plot_fractals_degreehigher_indicator(fractal_dn_color_higher, fractal_up_color_higher, fractal_degreehigher_marker_size, fractal_up_marker_higher, fractal_dn_marker_higher, FHH, FLH, main_plot_panel_id, data_last_selection, fractal_offset_value)



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
        addplot.append(price_peak_above_plot)
        addplot.append(price_peak_bellow_plot)
        
    #get date time of the last bar
    last_bar_dt = data_last_selection.index[-1]
    
    tittle_suffix = " " + str(len(data_last_selection)) +""
    
    chart_title = instrument + " \n" + timeframe 
    #+ tittle_suffix + "  " + str(last_bar_dt)
    subtitle = "" + get_dt_title_by_timeframe(last_bar_dt,timeframe)  + "      " + tittle_suffix
    
    
    colors = data_last_selection['zcol'].values
    #print(colors)
    #marketcolor_overrides=mco
    #print(data_last_selection)
    fmt = "%Y-%m-%d"
    if timeframe == "H1" or timeframe == "H4":
        fmt = "%y-%m-%d\n%H"
    if timeframe == "m5" or timeframe == "m15":
        fmt = "%y-%m-%d\n%H:%M"
    if timeframe == "M1":
        fmt = "%Y-%m"
    fig, axes = mpf.plot(
        ohlc,
        type=main_plot_type,
        style=plot_style,
        addplot=addplot,
        volume=False,
        figratio=(fig_ratio_x, fig_ratio_y),
        title=chart_title,
        returnfig=True,
        tight_layout=True,
        datetime_format=fmt,
        marketcolor_overrides=colors,
    )
    
    
    subtitle_x_pos = cc.subtitle_x_pos
    subtitle_y_pos = cc.subtitle_y_pos
    subtitle_ha = cc.subtitle_ha
    subtitle_fontsize = cc.subtitle_fontsize
    
    # Add subtitle to the first subplot
    axes[0].set_title(subtitle, fontsize=subtitle_fontsize, x=subtitle_x_pos,y=subtitle_y_pos, ha=subtitle_ha)  # Add subtitle to the first subplot
    
    # Set y-axis limits
    main_ymax, main_ymin = axes[main_plot_panel_id].get_ylim()
    height_minmax = main_ymax - main_ymin
    tst_v = height_minmax / 8
    new_y_max = main_ymin - tst_v - fdb_offset_value
    new_y_min = main_ymax + tst_v + fdb_offset_value

    
    axes[main_plot_panel_id].set_ylim(
        new_y_min,
        new_y_max
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
    fig.suptitle(chart_title, x=cc.title_x_pos, y=cc.title_y_pos, ha=cc.title_ha, fontsize=cc.title_fontsize)
 

    
    # Remove the y-axis label from the first subplot
    axes[0].set_ylabel('')
    axes[1].set_ylabel('')
    axes[2].set_ylabel('')
    
    # Remove the labels from the y-axis of the AO and AC plots
    axes[1].set_yticklabels([])
    axes[2].set_yticklabels([])
    
    axes[1].set_yticklabels([])
    axes[2].set_yticklabels([])
    
    show_grid = cc.show_grid
    # Set the font size of the Date column
    axes[main_plot_panel_id].tick_params(axis="x", labelsize=6)
    
    #@STCIssue Enlarging the canvas on top and right
    #fig.subplots_adjust(left=0.25, right=0.95, top=0.95, bottom=0.35)
    
    
    # Set the font size of the x-axis labels
    for ax in axes:
        ax.tick_params(axis="x", labelsize=6)
        ax.tick_params(axis="y", labelsize=5)
        
        
        ax.grid(show_grid)
    if show:
        plt.show()
    return fig,axes,data_last_selection

def _make_alligator_line_plots(jaw_color, teeth_color, lips_color, JAW, TEETH, LIPS, main_plot_panel_id, data_last_selection):
    jaw_plot = mpf.make_addplot(data_last_selection[JAW], panel=main_plot_panel_id, color=jaw_color)
    teeth_plot = mpf.make_addplot(data_last_selection[TEETH], panel=main_plot_panel_id, color=teeth_color)
    lips_plot = mpf.make_addplot(data_last_selection[LIPS], panel=main_plot_panel_id, color=lips_color)
    return jaw_plot,teeth_plot,lips_plot




#%% Too short plotting alternative 


def plot_from_cds_df_ALT(data,instrument:str,timeframe:str,show:bool=True,plot_ao_peaks:bool=True,cc: JGTChartConfig=None):
    
    """
    Plot OHLC bars, indicators, and signals from a pandas DataFrame.

    Args:
        data (pandas.DataFrame): The input DataFrame containing OHLC data.
        instrument (str): The instrument symbol.
        timeframe (str): The timeframe of the data.
        show (bool, optional): Whether to display the plot. Defaults to True.
        plot_ao_peaks (bool, optional): Whether to plot AO peaks. Defaults to False.
        cc (JGTChartConfig, optional): The chart configuration object. Defaults to None.

    Returns:
        fig: The figure object of the plot.
        axes: The axes object of the plot.
    """
    if cc is None:
        cc= JGTChartConfig()
   
    
    nb_bar_on_chart = cc.nb_bar_on_chart
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
    
        
    
    fig_ratio_x = cc.fig_ratio_x
    fig_ratio_y = cc.fig_ratio_y
    
    fdb_signal_buy_color = cc.fdb_signal_buy_color
    fdb_signal_sell_color = cc.fdb_signal_sell_color
    jaw_color = cc.jaw_color
    teeth_color = cc.teeth_color
    lips_color = cc.lips_color
    fractal_up_color = cc.fractal_up_color
    fractal_dn_color = cc.fractal_dn_color
    fractal_dn_color_higher = cc.fractal_dn_color_higher
    fractal_up_color_higher = cc.fractal_up_color_higher
    ac_signal_buy_color = cc.ac_signal_buy_color
    ac_signal_sell_color = cc.ac_signal_sell_color
    fdb_marker_size = cc.fdb_marker_size
    fractal_marker_size = cc.fractal_marker_size
    saucer_marker_size = cc.saucer_marker_size
    fractal_degreehigher_marker_size = cc.fractal_degreehigher_marker_size
    fdb_signal_marker = cc.fdb_signal_marker
    fractal_up_marker = cc.fractal_up_marker
    fractal_up_marker_higher = cc.fractal_up_marker_higher
    fractal_dn_marker_higher = cc.fractal_dn_marker_higher
    fractal_dn_marker = cc.fractal_dn_marker
    plot_style = cc.plot_style
    saucer_buy_color = cc.saucer_buy_color
    saucer_sell_color = cc.saucer_sell_color
    saucer_marker = cc.saucer_marker
    price_peak_bellow_marker = cc.price_peak_bellow_marker
    price_peak_above_marker = cc.price_peak_above_marker
    price_peak_marker_size = cc.price_peak_marker_size
    price_peak_above_color = cc.price_peak_above_color
    price_peak_bellow_color = cc.price_peak_bellow_color
    
    ac_signals_marker_size = cc.ac_signals_marker_size
    ac_signal_marker = cc.ac_signal_marker
    
    acb_plot_type =  cc.acb_plot_type
    
    ao_peaks_marker_size = cc.ao_peaks_marker_size
    ao_peak_offset_value = cc.ao_peak_offset_value
    ao_peak_above_marker_higher = cc.ao_peak_above_marker_higher
    ao_peak_bellow__marker_higher = cc.ao_peak_bellow__marker_higher
    aop_bellow_color = cc.aop_bellow_color
    aop_above_color = cc.aop_above_color
    
    #COLUMNS
    JAW = c.JAW
    TEETH = c.TEETH
    LIPS = c.LIPS
    
    OPEN = c.OPEN
    HIGH = c.HIGH
    LOW = c.LOW
    CLOSE = c.CLOSE
    BAR_HEIGHT = c.BAR_HEIGHT #"bar_height"
    
    FH = c.FH
    FL = c.FL
    FHH = c.FH8
    FLH = c.FL8
    
    
    FDB = c.FDB
    FDBB = c.FDBB
    FDBS = c.FDBS
    
    
    ACB = c.ACB  
    ACS = c.ACS
    
    #plot config
    main_plot_panel_id=cc.main_plot_panel_id
    ao_plot_panel_id=cc.ao_plot_panel_id
    ac_plot_panel_id=cc.ac_plot_panel_id
    
    
    
    #%% Select the last 400 bars of the data
    
    data_last_selection = data
    # Select the last 400 bars of the data
    tst_len_data = len(data)
    if nb_bar_on_chart != tst_len_data:    
        data_last_selection = _select_charting_nb_bar_on_chart(data, nb_bar_on_chart)
    l_datasel = len(data_last_selection)
    
    # Make OHLC bars plot
    ohlc = data_last_selection[[OPEN, HIGH, LOW, CLOSE]]
        
    #get date time of the last bar
    last_bar_dt = data_last_selection.index[-1]
    
    tittle_suffix = " " + str(len(data_last_selection)) +""
    
    chart_title = instrument + " \n" + timeframe 
    #+ tittle_suffix + "  " + str(last_bar_dt)
    subtitle = "" + get_dt_title_by_timeframe(last_bar_dt,timeframe)  + "      " + tittle_suffix
    
    
    fig, axes = mpf.plot(
        ohlc,
        type=main_plot_type,
        style=plot_style,
        #addplot=addplot,
        volume=False,
        figratio=(fig_ratio_x, fig_ratio_y),
        title=chart_title,
        returnfig=True,
        tight_layout=True,
    )
    
    # Add subtitle to the first subplot
    axes[0].set_title(subtitle, fontsize=10, x=0.07, ha="left")  # Add subtitle to the first subplot
    
    # # Set y-axis limits
    # main_ymax, main_ymin = axes[main_plot_panel_id].get_ylim()
    # height_minmax = main_ymax - main_ymin
    # tst_v = height_minmax / 8
    # new_y_max = main_ymin - tst_v - fdb_offset_value
    # new_y_min = main_ymax + tst_v + fdb_offset_value
    
    
    # axes[main_plot_panel_id].set_ylim(
    #     new_y_min,
    #     new_y_max
    # )
        
    #       low_min - fdb_offset_value - pipsize * 30,
    #       high_max + fdb_offset_value+ pipsize * 33
    #   )
        
    #       low_min - fdb_offset_value - pipsize * 330,
    #       high_max + fdb_offset_value + pipsize * 330,
    #   )

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
    fig.suptitle(chart_title, x=0.05, ha="left")
    #fig.subtitle("oeuoeuoeu", x=0.15, ha="left")

    # Set the font size of the x-axis labels
    for ax in axes:
        ax.tick_params(axis="x", labelsize=6)

    # Set the font size of the Date column
    axes[main_plot_panel_id].tick_params(axis="x", labelsize=6)

    if show:
        plt.show()
    return fig,axes,data_last_selection
    





def get_dt_title_by_timeframe(last_bar_dt, timeframe, separator="/"):
    format_str = {
        'M1': f'%y{separator}%m',  # Year-Month
        'W1': f'%y{separator}%m{separator}%d',  # Year-Week number
        'D1': f'%y{separator}%m{separator}%d',  # Year-Month-Day
        'H8': f'%y{separator}%m{separator}%d %H',  # Year-Month-Day Hour
        'H6': f'%y{separator}%m{separator}%d %H',  # Year-Month-Day Hour
        'H4': f'%y{separator}%m{separator}%d %H',  # Year-Month-Day Hour
        'H3': f'%y{separator}%m{separator}%d %H',  # Year-Month-Day Hour
        'H2': f'%y{separator}%m{separator}%d %H',  # Year-Month-Day Hour
        'H1': f'%y{separator}%m{separator}%d %H',  # Year-Month-Day Hour
        'm30': f'%y{separator}%m{separator}%d %H:%M',  # Year-Month-Day Hour:Minute
        'm15': f'%y{separator}%m{separator}%d %H:%M',  # Year-Month-Day Hour:Minute
        'm5': f'%y{separator}%m{separator}%d %H:%M'  # Year-Month-Day Hour:Minute
    }.get(timeframe, f'%Y{separator}%m{separator}%d %H:%M')  # Default to full date-time if timeframe is not recognized

    return last_bar_dt.strftime(format_str)


def _select_charting_nb_bar_on_chart(data, nb_bar_on_chart):
    try:
        data_last_selection = data.iloc[-nb_bar_on_chart:].copy()
        #data_last_selection.to_csv("out_data_last_selection.csv")
    except:
        l.warning("Could not select the desired amount of bars, trying anyway with what we have")
        data_last_selection = data
        pass
    return data_last_selection




def make_plot__price_peaks__indicator(price_peak_above_color, price_peak_bellow_color, price_peak_marker_size, price_peak_above_marker, price_peak_bellow_marker, price_peak_above_coln, price_peak_bellow_coln, main_plot_panel_id, data_last_selection, price_peak_offset_value):
    price_peak_above_plot = mpf.make_addplot(
      data_last_selection[price_peak_above_coln] + price_peak_offset_value,
      panel=main_plot_panel_id,
      type="scatter",
      markersize=price_peak_marker_size,
      marker=price_peak_above_marker,
      color=price_peak_above_color,
  )
    price_peak_bellow_plot= mpf.make_addplot(
      data_last_selection[price_peak_bellow_coln] - price_peak_offset_value,
      panel=main_plot_panel_id,
      type="scatter",
      markersize=price_peak_marker_size,
      marker=price_peak_bellow_marker,
      color=price_peak_bellow_color,
  )
    return price_peak_above_plot,price_peak_bellow_plot

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
      data_last_selection[fl_col_dim_higher] - fractal_offset_value,
      panel=main_plot_panel_id,
      type="scatter",
      markersize=fractal_degreehigher_marker_size,
      marker=fractal_dn_marker_higher,
      color=fractal_dn_color_higher,
  )
    
    return fractal_up_plot_higher,fractal_down_plot_higher



def make_plot__ao_ac(data:pd.DataFrame,cc: JGTChartConfig=None, ao_plot_panel_id=1, ac_plot_panel_id=2):
    if cc is None:
        cc = JGTChartConfig()
    # ao_upbar_color, ao_dnbar_color, ac_up_color, ac_dn_color
    ao_upbar_color = cc.ao_upbar_color
    ao_dnbar_color = cc.ao_dnbar_color
    ac_up_color = cc.ac_up_color
    ac_dn_color = cc.ac_dn_color
    ao_plot_type = cc.ao_plot_type
    ac_plot_type = cc.ac_plot_type
    
    # Calculate the color for 'ao' and 'ac' bar
    colors_ao = [
        ao_upbar_color if (data.iloc[i][AO] - data.iloc[i - 1][AO] > 0) else ao_dnbar_color
        for i in range(1, len(data[AO]))
    ]
    colors_ao.insert(0, ao_dnbar_color)

    colors_ac = [
        ac_up_color
        if (data.iloc[i][AC] - data.iloc[i - 1][AC] > 0)
        else ac_dn_color
        for i in range(1, len(data))
    ]
    colors_ac.insert(0, ac_dn_color)
    
    # Make 'ao' and 'ac' oscillator plot
    
    ao_plot = mpf.make_addplot(
        data[AO], panel=ao_plot_panel_id, color=colors_ao, secondary_y=False, type=ao_plot_type,
        #label="AO"
    )
    #ao_plot.subplots_adjust(left=0.25, right=0.95, top=0.95, bottom=0.15)
    
    ac_plot = mpf.make_addplot(
        data[AC], panel=ac_plot_panel_id, color=colors_ac, secondary_y=False, type=ac_plot_type,
        #label="AC"
    )
    
    return ao_plot, ac_plot



def make_plot__fractals_indicator(fractal_up_color, fractal_dn_color, fractal_marker_size, fractal_up_marker, fractal_dn_marker, fh_col_dim, fl_col_dim, main_plot_panel_id, data_last_selection, fractal_offset_value, fractals_plot_type="scatter"):
    fractal_up_plot = mpf.make_addplot(
        data_last_selection[fh_col_dim] + fractal_offset_value,
        panel=main_plot_panel_id,
        type=fractals_plot_type,
        markersize=fractal_marker_size,
        marker=fractal_up_marker,
        color=fractal_up_color,
)
    fractal_down_plot = mpf.make_addplot(
        data_last_selection[fl_col_dim] - fractal_offset_value,
        panel=main_plot_panel_id,
        type=fractals_plot_type,
        markersize=fractal_marker_size,
        marker=fractal_dn_marker,
        color=fractal_dn_color,
)    
    return fractal_up_plot,fractal_down_plot


def make_plot__fdb_signals(fdb_signal_buy_color, fdb_signal_sell_color, fdb_marker_size, fdb_signal_marker, fdbb_coln, fdbs_coln, main_plot_panel_id, data_last_selection, fdb_offset_value,fdb_plot_type = "scatter"):
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
                fdbs_plot_type (str, optional): Plot type for sell signals. Defaults to "scatter".

        Returns:
                tuple: A tuple containing the scatter plot for buy signals and the scatter plot for sell signals.
        """
        
        fdbb_up_plot = make_plot_fdbb_signal(fdb_signal_buy_color, fdb_marker_size, fdb_signal_marker, fdbb_coln, main_plot_panel_id, data_last_selection, fdb_offset_value,fdb_plot_type)

        fdbs_down_plot = make_plot_fdbs_signal(fdb_signal_sell_color, fdb_marker_size, fdb_signal_marker, fdbs_coln, main_plot_panel_id, data_last_selection, fdb_offset_value,fdb_plot_type)
        
        return fdbb_up_plot,fdbs_down_plot

def make_plot_fdbs_signal(fdb_signal_sell_color, fdb_marker_size, fdb_signal_marker, fdbs_coln, main_plot_panel_id, data_last_selection, fdb_offset_value,fdbs_plot_type = "scatter"):
    
    fdbs_down_plot = mpf.make_addplot(
            data_last_selection[fdbs_coln] - fdb_offset_value,
            panel=main_plot_panel_id,
            type=fdbs_plot_type,
            markersize=fdb_marker_size,
            marker=fdb_signal_marker,
            color=fdb_signal_sell_color,
    )

    return fdbs_down_plot

def make_plot_fdbb_signal(fdb_signal_buy_color, fdb_marker_size, fdb_signal_marker, fdbb_coln, main_plot_panel_id, data_last_selection, fdb_offset_value,fdbb_plot_type = "scatter"):
    
    fdbb_up_plot = mpf.make_addplot(
            data_last_selection[fdbb_coln] + fdb_offset_value,
            panel=main_plot_panel_id,
            type=fdbb_plot_type,
            markersize=fdb_marker_size,
            marker=fdb_signal_marker,
            color=fdb_signal_buy_color,
    )

    return fdbb_up_plot
  #return plt


# %% ALias function (future name)

def plotcdf(data,instrument, timeframe, show=True,plot_ao_peaks=True,cc: JGTChartConfig=None):
  return plot_from_cds_df(data,instrument,timeframe,show=show,plot_ao_peaks=plot_ao_peaks,cc=cc)


def plot_perspective(rq:JGTADSRequest):
    #timeframes = rq.timeframes.split(",")
    perspective={}
    perspective["rq"] = rq
    for tf in rq.timeframes:
        #instanciate a copy of the request
        _rq = rq.copy_with_timeframe(tf)
        _c,_a,_d=plot_v2(_rq,BETA_TRY=True)
        _p={}
        _p = {
            "fig": _c,
            "axes": _a,
            "data": _d,
            "rq": _rq
        }
        perspective[tf] = _p
        #{"fig":_c,"axes":_a,"data":_d,"request":_rq}
    return perspective

def plot_v2(rq:JGTADSRequest,BETA_TRY=False):
    if BETA_TRY:
        return plot(rq=rq)
    # (rq.instrument,
    #                 rq.timeframe,
    #                 show=rq.show,
    #                 plot_ao_peaks=rq.plot_ao_peaks,
    #                 crop_last_dt=rq.crop_last_dt,
    #                 use_fresh=rq.use_fresh,
    #                 cc=rq.cc)
    else:
        raise Exception("Not implemented yet")
    

def plot(instrument:str=None,
         timeframe:str=None,
         show:bool=True,
         plot_ao_peaks:bool=True,
         cc: JGTChartConfig=None,
         tlid_range:str=None,
         crop_last_dt:str=None,
         use_fresh=False,
         rq:JGTADSRequest=None):
    """
    Plot the chart for a given instrument and timeframe.

    Parameters:
    instrument (str): The name of the instrument.
    timeframe (str): The timeframe for the chart.
    show (bool, optional): Whether to display the plot. Default is True.
    plot_ao_peaks (bool, optional): Whether to plot AO peaks. Defaults to True.
    cc (JGTChartConfig, optional): The chart configuration object. Defaults to None.
    tlid_range (str, optional): The range of TLIDs to use for the plot. Defaults to None. (WE WILL USE crop_last_dt INSTEAD or we might split and transform it for using it as crop_last_dt...)
    crop_last_dt (str, optional): The last date-time to crop the data. Defaults to None.
    use_fresh (bool, optional): Whether to use fresh data. Defaults to False.
    rq (JGTADSRequest, optional): The request object. Defaults to None.
    
    Returns:
    fig: The figure object of the plot.
    axes: The axes object of the plot.
    cdfdata: The CDF data used for the plot (and made in the process
    """
    if rq is not None:
        use_fresh = rq.use_fresh
        cc = rq.cc
        crop_last_dt = rq.crop_last_dt
        tlid_range = rq.tlid_range
        plot_ao_peaks = rq.plot_ao_peaks
        show = rq.show
        if instrument is None:
            instrument = rq.instrument
        if timeframe is None:
            timeframe = rq.timeframe
    
    fig, axes,cdfdata = jgtxplot18c_231209(instrument, timeframe, show=show,plot_ao_peaks=plot_ao_peaks,cc=cc,tlid_range=tlid_range,crop_last_dt=crop_last_dt,use_fresh=use_fresh,rq=rq)
    
    return fig, axes,cdfdata

  
