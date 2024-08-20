#!/usr/bin/env python
# 
# # @title ADS

# Imports
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt
import mplfinance as mpf

import traceback

import sys
import os



# COLUMNS
from jgtutils.jgtconstants import (
    JAW,
    TEETH,
    LIPS,
    OPEN,
    HIGH,
    LOW,
    CLOSE,
    VOLUME,
    BAR_HEIGHT,
    FH,
    FL,
    FDB,
    FDBB,
    FDBS,
    ACB,
    ACS,
    SB,
    SS,
    AO,
    AC,
    PRICE_PEAK_ABOVE,
    PRICE_PEAK_BELLOW,
    AO_PEAK_ABOVE,
    AO_PEAK_BELLOW,
)

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from jgtutils.jgtos import ensure_directory_exists

from jgtpyhelper import get_dt_fmt_for_timeframe


# import jgtpy
import JGTPDSP as pds  # Should be managed by cds
#import JGTIDS as ids
#from JGTIDS import getMinByTF
import JGTCDS as cds


# @STCGoal Unified JGTChartConfig & JGTADSRequest
from JGTChartConfig import JGTChartConfig
from JGTADSRequest import JGTADSRequest
import JGTChartConfig as CC
import JGTADSRequest as RQ

import adshelper as ah

warnings.filterwarnings("ignore", category=FutureWarning)



# import kaleido
# import plotly

import JGTConfig as jgtc


# import plotly.graph_objects as go
# import plotly.subplots as sp



#from jgtutils import jgtlogging as l
import logging
l = logging.getLogger(__name__)


cdtformat = "%Y-%m-%d"



def jgtxplot18c_231209(
    instrument: str,
    timeframe: str,
    show: bool = True,
    plot_ao_peaks: bool = True,
    cc: JGTChartConfig = None,
    tlid_range: str = None,
    crop_last_dt: str = None,
    use_fresh=False,
    rq: JGTADSRequest = None,
)->{Figure,list,pd.DataFrame}:

    data = ah.prepare_cds_for_ads_data(
        instrument,
        timeframe,
        tlid_range=tlid_range,
        cc=cc,
        crop_last_dt=crop_last_dt,
        use_fresh=use_fresh,
        rq=rq,
    )  # @STCGoal Supports TLID
    # @STCIssue Desired Number of Bars ALREADY SELECTED IN THERE
    # print(len(data))
    # data.to_csv("debug_data" + instrument.replace("/","-") + timeframe + ".csv")
    fig,axes,cdfdata=None,None,None
    try:
        fig, axes, cdfdata = plot_from_cds_df(
            data,
            instrument,
            timeframe,
            show=show,
            plot_ao_peaks=plot_ao_peaks,
            cc=cc,
            rq=rq        )
        if fig is not None:
            return fig, axes, cdfdata
    except Exception as e:
        if fig is not None:
            print("   Fig is not none so we return it and wont try the ALT")
            return fig, axes, cdfdata
        if rq is not None and rq.verbose_level> 1:
            print("Error plotting regular ADS for:" + instrument + " " + timeframe + ", exception: " + str(e))
            traceback.print_exc()
        print("ALT Plotting (" + instrument + " " + timeframe + ")" )
        try:
            return plot_from_cds_df_ALT(
            data, instrument, timeframe, show=show, cc=cc, rq=rq
        )
        except Exception as e2:
            print("ALT Plotting Failed. ", str(e2))
            traceback.print_exc()
            raise e2


def plot_from_pds_df(
    pdata,
    instrument: str,
    timeframe: str,
    show: int = True,
    plot_ao_peaks=True,
    cc: JGTChartConfig = None,
    tlid_range: str = None,
    rq: JGTADSRequest = None,
)->{Figure,list,pd.DataFrame}:
    if rq is not None:
        cc = rq.cc
    if cc is None:
        cc = JGTChartConfig()
    if rq is None:
        rq = JGTADSRequest(cc=cc)

    cds_required_amount_of_bar_for_calc = cc.cds_required_amount_of_bar_for_calc
    nb_bar_on_chart = cc.nb_bar_on_chart

    # Select the last cds_required_amount_of_bar_for_calc
    # @STCIssue Desired Number of Bars MUST SUPPORT TLID RANGE
    try:
        selected = pdata.iloc[
            -nb_bar_on_chart - cds_required_amount_of_bar_for_calc :
        ].copy()  # @STCGoal A Unified way to select the data
    except:
        selected = pdata.copy()
        l.warning(
            "Could not select the desired amount of bars, trying anyway with what we have"
        )
        pass

    data1 = cds.createFromDF(selected, cc=cc, quiet=rq.quiet, rq=rq)

    # @STCGoal Make sure we have the amount of bars we were requested (and not more)
    try:
        data = data1.iloc[-nb_bar_on_chart:].copy()
    except:
        data = data1.copy()
        l.warning(
            "Could not select the desired amount of bars, trying anyway with what we have"
        )
        pass
    return plot_from_cds_df(
        data,
        instrument,
        timeframe,
        show=show,
        plot_ao_peaks=plot_ao_peaks,
        cc=cc,
        rq=rq,
    )
    


def plot_from_cds_df(
    data: pd.DataFrame,
    instrument: str,
    timeframe: str,
    show=True,
    plot_ao_peaks: bool = True,
    cc: JGTChartConfig = None,
    rq: JGTADSRequest = None,
)->{Figure,list,pd.DataFrame}:
    """
    Plot OHLC bars, indicators, and signals from a pandas DataFrame.

    Args:
        data (pandas.DataFrame): The input DataFrame containing OHLC data.
        instrument (str): The instrument symbol.
        timeframe (str): The timeframe of the data.
        show (bool, optional): Whether to display the plot. Defaults to True.
        plot_ao_peaks (bool, optional): Whether to plot AO peaks. Defaults to False.
        cc (JGTChartConfig, optional): The chart configuration object. Defaults to None.
        rq (JGTADSRequest, optional): The request object. Defaults to None.

    Returns:
        fig: The figure object of the plot.
        axes: The axes object of the plot.
    """
    if rq is not None:
        cc = rq.cc
    if cc is None:
        cc = JGTChartConfig()
    if rq is None:
        rq = JGTADSRequest()

    fhh = FH + str(cc.fractal_high_degree)
    flh = FL + str(cc.fractal_high_degree)
    fuhh = FH + str(cc.fractal_ultra_high_degree)
    fulh = FL + str(cc.fractal_ultra_high_degree)

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

    # fig_ratio_x = cc.fig_ratio_x
    # fig_ratio_y = cc.fig_ratio_y

    # fdb_signal_buy_color = cc.fdb_signal_buy_color
    # fdb_signal_sell_color = cc.fdb_signal_sell_color
    # jaw_color = cc.jaw_color
    # teeth_color = cc.teeth_color
    # lips_color = cc.lips_color
    # fractal_up_color = cc.fractal_up_color
    # fractal_dn_color = cc.fractal_dn_color
    # fractal_dn_color_higher = cc.fractal_dn_color_higher
    # fractal_up_color_higher = cc.fractal_up_color_higher
    # ac_signal_buy_color = cc.ac_signal_buy_color
    # ac_signal_sell_color = cc.ac_signal_sell_color
    # fdb_marker_size = cc.fdb_marker_size
    # fractal_marker_size = cc.fractal_marker_size
    # saucer_marker_size = cc.saucer_marker_size
    # fractal_degreehigher_marker_size = cc.fractal_degreehigher_marker_size
    # fdb_signal_marker = cc.fdb_signal_marker
    # fractal_up_marker = cc.fractal_up_marker
    # fractal_up_marker_higher = cc.fractal_up_marker_higher
    # fractal_dn_marker_higher = cc.fractal_dn_marker_higher
    # fractal_dn_marker = cc.fractal_dn_marker
    # plot_style = cc.plot_style
    # saucer_buy_color = cc.saucer_buy_color
    # saucer_sell_color = cc.saucer_sell_color
    # saucer_marker = cc.saucer_marker
    # price_peak_bellow_marker = cc.price_peak_bellow_marker
    # price_peak_above_marker = cc.price_peak_above_marker
    # price_peak_marker_size = cc.price_peak_marker_size
    # price_peak_above_color = cc.price_peak_above_color
    # price_peak_bellow_color = cc.price_peak_bellow_color

    # ac_signals_marker_size = cc.ac_signals_marker_size
    # ac_signal_marker = cc.ac_signal_marker

    # acb_plot_type = cc.acb_plot_type

    # ao_peaks_marker_size = cc.ao_peaks_marker_size
    # ao_peak_offset_value = cc.ao_peak_offset_value
    # ao_peak_above_marker_higher = cc.ao_peak_above_marker_higher
    # ao_peak_bellow__marker_higher = cc.ao_peak_bellow__marker_higher
    # aop_bellow_color = cc.aop_bellow_color
    # aop_above_color = cc.aop_above_color



    # # plot config
    main_plot_panel_id = cc.main_plot_panel_id
    ao_plot_panel_id = cc.ao_plot_panel_id
    ac_plot_panel_id = cc.ac_plot_panel_id

    # Select the last 400 bars of the data

    data_last_selection:pd.DataFrame = data
    # Select the last 400 bars of the data
    tst_len_data = len(data)
    if nb_bar_on_chart != tst_len_data: #@STCIssue Isn't this already done ???
        data_last_selection = _select_charting_nb_bar_on_chart(data, nb_bar_on_chart)
    l_datasel = len(data_last_selection)
    desired_number_of_bars=l_datasel>=nb_bar_on_chart

    # Make OHLC bars plot
    ohlc = data_last_selection[[OPEN, HIGH, LOW, CLOSE]]

    # Plotting
    addplot = []

    # AO/AC
    # AO / AC Plotting
    if cc.show_ao == False:
        ac_plot_panel_id = 1 #AC Plot becomes second

    # @STCGoal Make AO/AC signals plotted
    
    if cc.show_ao:
        ao_plot = make_plot__ao(data_last_selection, 
                                     cc, 
                                     ao_plot_panel_id)
        addplot.append(ao_plot)
    
    if cc.show_ac:
        ac_plot = make_plot__ac(data_last_selection, 
                                     cc, 
                                     ac_plot_panel_id)
        addplot.append(ac_plot)
       
        


    # Alligator

    # @STCIssue no offset data in, not offset columns: jaws_tmp,teeth_tmp,lips_tmp

    # Make Alligator's lines plot
    if cc.show_alligator:
        jaw_plot, teeth_plot, lips_plot = make_alligator_plots(
                plot_panel_id=main_plot_panel_id,
                data=data_last_selection,
                cc=cc,
            )
        
        addplot.append(jaw_plot)
        addplot.append(teeth_plot)
        addplot.append(lips_plot)

    # Offsets and various values
    # offset

    # min_timeframe = getMinByTF(timeframe)
    # price_mean = data_last_selection[CLOSE].mean()

    # Calculate the bar height for each row
    data_last_selection[BAR_HEIGHT] = (
        data_last_selection[HIGH] - data_last_selection[LOW]
    )

    # Calculate the average bar height
    average_bar_height = data_last_selection[BAR_HEIGHT].mean()
    # low_min = data_last_selection[LOW].min()
    # high_max = data_last_selection[HIGH].max()


        
    # Date,Volume,Open,High,Low,Close,Median,ac,jaw,teeth,lips,bjaw,bteeth,blips,ao,fh,fl,fh3,fl3,fh5,fl5,fh8,fl8,fh13,fl13,fh21,fl21,fh34,fl34,fh55,fl55,fh89,fl89,fdbb,fdbs,fdb,aof,aoaz,aobz,zlc,zlcb,zlcs,zcol,sz,bz,acs,acb,ss,sb

    #  AO_PEAK_BELLOW  / AO_PEAK_BELLOW Plot
    if plot_ao_peaks and cc.show_ao and cc.show_ao_peaks:  

        # AO Peaks
        ao_max, ao_min = ao_max_min(data_last_selection)
        
        # Align AO Peaks with AO bars if value is '1.0'
        aopbellow_plot = make_ao_peak_bellow_plot(cc, ao_plot_panel_id, data_last_selection, ao_max)


        # Make AO Peak Above plot
        aopabove_plot = make_ao_peak_above_plot(cc, ao_plot_panel_id, data_last_selection, ao_min)
        
        addplot.append(aopabove_plot)
        addplot.append(aopbellow_plot)
        if rq.verbose_level> 1:
            print("Added AO ABove/Bellow Peaks plot")
        
        
    price_peak_offset_value = average_bar_height / 3 * 5
    
    # PRICE_PEAK_ABOVE / PRICE_PEAK_ABOVE
    if plot_ao_peaks and cc.show_price_peak:


        data_last_selection.loc[:, PRICE_PEAK_ABOVE] = np.where(
            data_last_selection[PRICE_PEAK_ABOVE] == 1.0,
            data_last_selection[HIGH],
            np.nan,
        )
        data_last_selection.loc[:, PRICE_PEAK_BELLOW] = np.where(
            data_last_selection[PRICE_PEAK_BELLOW] == 1.0,
            data_last_selection[LOW],
            np.nan,
        )

        price_peak_above_plot, price_peak_bellow_plot = (
            make_plot__price_peaks__indicator(
                cc.price_peak_above_color,
                cc.price_peak_bellow_color,
                cc.price_peak_marker_size,
                cc.price_peak_above_marker,
                cc.price_peak_bellow_marker,
                PRICE_PEAK_ABOVE,
                PRICE_PEAK_BELLOW,
                main_plot_panel_id,
                data_last_selection,
                price_peak_offset_value,
            )
        )
        
        addplot.append(price_peak_above_plot)
        addplot.append(price_peak_bellow_plot)
        if rq.verbose_level> 1:
            print("Added Price Peaks plot")
        



    if cc.show_ao and cc.show_saucer:
            
        saucer_offset_value = 0
        # Saucer
        
        # Align saucer with AO bars if value is '1.0'
        sb_plot = make_saucer_buy_plot(cc, ao_plot_panel_id, data_last_selection, ao_max, saucer_offset_value)

        ss_plot = make_saucer_sell_plot(cc, ao_plot_panel_id, data_last_selection, ao_min, saucer_offset_value)
        
        addplot.append(sb_plot)
        addplot.append(ss_plot)
        
    

    #ac_max, ac_min = ac_max_min(data_last_selection)

    # AC Signal
    if cc.show_ac and cc.show_ac_signal:

        sig_ac_offset_value = 0

        # Align ACB with OHLC bars if value is '1.0'
        acb_plot = make_acb_plot(cc, ac_plot_panel_id, data_last_selection, sig_ac_offset_value)
        
        acs_plot = make_acs_plot(cc, ac_plot_panel_id, data_last_selection, sig_ac_offset_value)


        addplot.append(acb_plot)
        addplot.append(acs_plot)


     
    # FDB
    fdb_tick_offset = average_bar_height  # pipsize * 111
    fdb_offset_value = average_bar_height / 2  # pipsize * fdb_tick_offset
    if cc.show_fdb_signal:


           

        fdbb_up_plot, fdbs_down_plot = make_plot__fdb_signals(
            data=data_last_selection,
            fdb_offset_value=fdb_offset_value,
            cc=cc,
            plot_panel_id=main_plot_panel_id
            )
            
        
        addplot.append(fdbb_up_plot)
        addplot.append(fdbs_down_plot)
            
            
    fractal_offset_value = average_bar_height / 2  # pipsize * fractal_tick_offset
    
    # Make Fractals plot
    if cc.show_fractal:
            

        fractal_tick_offset = pipsize * 111  # price_mean*10

        # Align fractals with OHLC bars

        data_last_selection.loc[:, FH] = np.where(
            (data_last_selection[HIGH] > data_last_selection[TEETH])
            & (data_last_selection[FH] == True),
            data_last_selection[HIGH],
            np.nan,
        )

        data_last_selection.loc[:, FL] = np.where(
            (data_last_selection[LOW] < data_last_selection[TEETH])
            & (data_last_selection[FL] == True),
            data_last_selection[LOW] - fractal_offset_value,
            np.nan,
        )

        fractal_up_plot, fractal_down_plot = make_plot__fractals_indicator(
            cc.fractal_up_color,
            cc.fractal_dn_color,
            cc.fractal_marker_size,
            cc.fractal_up_marker,
            cc.fractal_dn_marker,
            FH,
            FL,
            main_plot_panel_id,
            data_last_selection,
            fractal_offset_value,
        )
        
        addplot.append(fractal_up_plot)
        addplot.append(fractal_down_plot)
        if rq.verbose_level> 1:
            print("Added Fractal plot")
        

    # Fractal higher dim
    # @STCIssue The Data IS not Prepared in the PLot Maker.  Is this a problem? Should it be? Should it be done here or into a  function preparing the data for the plot? That way we could use it for more plot Types.
    
    if cc.show_fractal_higher:
            
        data_last_selection.loc[:, fhh] = np.where(
            (data_last_selection[HIGH] > data_last_selection[TEETH])
            & (data_last_selection[fhh] == True),
            data_last_selection[HIGH],
            np.nan,
        )

        data_last_selection.loc[:, flh] = np.where(
            (data_last_selection[LOW] < data_last_selection[TEETH])
            & (data_last_selection[flh] == True),
            data_last_selection[LOW] - fractal_offset_value,
            np.nan,
        )

        # PLot higher fractal

        fractal_up_plot_higher, fractal_down_plot_higher = (
            make_plot_fractals_degreehigher_indicator(
                cc.fractal_dn_color_higher,
                cc.fractal_up_color_higher,
                cc.fractal_degreehigher_marker_size,
                cc.fractal_up_marker_higher,
                cc.fractal_dn_marker_higher,
                fhh,
                flh,
                main_plot_panel_id,
                data_last_selection,
                fractal_offset_value,
            )
        )
        
        addplot.append(fractal_up_plot_higher)
        addplot.append(fractal_down_plot_higher)
        if rq.verbose_level> 1:
            print("Added Fractal Higher plot")

    
    if cc.show_fractal_ultra_higher:
            
        data_last_selection.loc[:, fuhh] = np.where(
            (data_last_selection[HIGH] > data_last_selection[TEETH])
            & (data_last_selection[fuhh] == True),
            data_last_selection[HIGH],
            np.nan,
        )

        data_last_selection.loc[:, fulh] = np.where(
            (data_last_selection[LOW] < data_last_selection[TEETH])
            & (data_last_selection[fulh] == True),
            data_last_selection[LOW] - fractal_offset_value,
            np.nan,
        )

        # PLot ultra higher fractal
   
        
        fractal_up_plot_ultra_higher, fractal_down_plot_ultra_higher = (
            make_plot_fractals_by_degree_UNIFIED(
                cc.fractal_dn_color_ultra_higher,
                cc.fractal_up_color_ultra_higher,
                cc.fractal_degreehigher_marker_size,
                cc.fractal_up_marker_higher,
                cc.fractal_dn_marker_higher,
                main_plot_panel_id,
                data_last_selection,
                fractal_offset_value,
                fractal_dim=cc.fractal_ultra_high_degree
            )
        )

        addplot.append(fractal_up_plot_ultra_higher)
        addplot.append(fractal_down_plot_ultra_higher)
        if rq.verbose_level> 1:
            print("Added Fractal Ultra higher plot")


       
    
    #print("addplot dict : " + str(addplot))

    # get date time of the last bar
    last_bar_dt = data_last_selection.index[-1]

    tittle_suffix = " " + str(len(data_last_selection)) + ""

    chart_title = instrument + " \n" + timeframe
    # + tittle_suffix + "  " + str(last_bar_dt)
    subtitle = (
        ""
        + get_dt_title_by_timeframe(last_bar_dt, timeframe)
        + "      "
        + tittle_suffix
    )

    if rq.verbose_level> 1:
        print("Chart title is :", chart_title," - ",subtitle)
    
    colors = data_last_selection["zcol"].values
    # print(colors)
    # marketcolor_overrides=mco
    # print(data_last_selection)
    
    fmt = get_dt_fmt_for_timeframe(timeframe)

    if rq.verbose_level> 1:
        print("Chart fmt :",fmt)
    fig:Figure=None
    axes:list=None
    fig, axes = mpf.plot(
        ohlc,
        type=cc.main_plot_type,
        style=cc.plot_style,
        addplot=addplot if len(addplot) > 0 else None,
        volume=False,
        figratio=(cc.fig_ratio_x, cc.fig_ratio_y),
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
    axes[0].set_title(
        subtitle,
        fontsize=subtitle_fontsize,
        x=subtitle_x_pos,
        y=subtitle_y_pos,
        ha=subtitle_ha,
    )  # Add subtitle to the first subplot

    # Set y-axis limits
    main_ymax, main_ymin = axes[main_plot_panel_id].get_ylim()
    height_minmax = main_ymax - main_ymin
    tst_v = height_minmax / 8
    new_y_max = main_ymin - tst_v - fdb_offset_value
    new_y_min = main_ymax + tst_v + fdb_offset_value

    axes[main_plot_panel_id].set_ylim(new_y_min, new_y_max)

    # Get current x-axis limits
    x_min, x_max = axes[main_plot_panel_id].get_xlim()

    if cc.show_ac:
        ac_axe2ymin, ac_axe2ymax = axes[ac_plot_panel_id].get_ylim()
        l.debug("axe2ymin: " + str(ac_axe2ymin))
        l.debug("axe2ymax: " + str(ac_axe2ymax))

    # Calculate new x-axis limit
    new_x_max = x_max + 8  # Add 8 for future bars

    # Set new x-axis limit
    axes[main_plot_panel_id].set_xlim(x_min, new_x_max)

    # Align the title to the left
    fig.suptitle(
        chart_title,
        x=cc.title_x_pos,
        y=cc.title_y_pos,
        ha=cc.title_ha,
        fontsize=cc.title_fontsize,
    )

    # Remove the y-axis label from the first subplot
    axes[main_plot_panel_id].set_ylabel("")
    if cc.show_ao:
        axes[ao_plot_panel_id].set_ylabel("")
    if cc.show_ac:
        axes[ac_plot_panel_id].set_ylabel("")

    # Remove the labels from the y-axis of the AO and AC plots
    if cc.show_ao:
        axes[ao_plot_panel_id].set_yticklabels([])
    if cc.show_ac:
        axes[ac_plot_panel_id].set_yticklabels([])

    if cc.show_ao:
        axes[ao_plot_panel_id].set_yticklabels([])
    if cc.show_ac:
        axes[ac_plot_panel_id].set_yticklabels([])

    show_grid = cc.show_grid
    # Set the font size of the Date column
    axes[main_plot_panel_id].tick_params(axis="x", labelsize=6)

    # @STCIssue Enlarging the canvas on top and right
    # fig.subplots_adjust(left=0.25, right=0.95, top=0.95, bottom=0.35)

    # Set the font size of the x-axis labels
    for ax in axes:
        ax.tick_params(axis="x", labelsize=6)
        ax.tick_params(axis="y", labelsize=5)

        ax.grid(show_grid)

    if rq.save_additional_figures_path is not None or rq.save_figure_as_timeframe:
        save_add_figure(instrument, timeframe, rq, fig)

    if show:
        plt.show()
    return fig, axes, data_last_selection








def make_saucer_buy_plot(cc, ao_plot_panel_id, data_last_selection, ao_max, saucer_offset_value):
    data_last_selection.loc[:, SB] = np.where(
            data_last_selection[SB] == 1.0, ao_max, np.nan
        )


        # Make Buy Signal plot

    sb_plot = mpf.make_addplot(
            data_last_selection[SB] + saucer_offset_value,
            panel=ao_plot_panel_id,
            type="scatter",
            markersize=cc.saucer_marker_size,
            marker=cc.saucer_marker,
            color=cc.saucer_buy_color,
        )
    
    return sb_plot

def make_saucer_sell_plot(cc, ao_plot_panel_id, data_last_selection, ao_min, saucer_offset_value):
    data_last_selection.loc[:, SS] = np.where(
            data_last_selection[SS] == 1.0, ao_min, np.nan
        )
        # Make Sell Signal plot
    ss_plot = mpf.make_addplot(
            data_last_selection[SS] - saucer_offset_value,
            panel=ao_plot_panel_id,
            type="scatter",
            markersize=cc.saucer_marker_size,
            marker=cc.saucer_marker,
            color=cc.saucer_sell_color,
        )
    
    return ss_plot

def make_acb_plot(cc, ac_plot_panel_id, data_last_selection, sig_ac_offset_value):
    data_last_selection.loc[:, ACB] = np.where(
            data_last_selection[ACB] == 1.0, data_last_selection[AC], np.nan
        )

        # Make Buy Signal plot
    acb_plot = mpf.make_addplot(
            data_last_selection[ACB] + sig_ac_offset_value,
            panel=ac_plot_panel_id,
            type=cc.acb_plot_type,
            markersize=cc.ac_signals_marker_size,
            marker=cc.ac_signal_marker,
            color=cc.ac_signal_buy_color,
        )
    
    return acb_plot

def make_acs_plot(cc, ac_plot_panel_id, data_last_selection, sig_ac_offset_value):
    data_last_selection.loc[:, ACS] = np.where(
            data_last_selection[ACS] == 1.0, data_last_selection[AC], np.nan
        )
        
        # Make Sell Signal plot
    acs_plot = mpf.make_addplot(
            data_last_selection[ACS] - sig_ac_offset_value,
            panel=ac_plot_panel_id,
            type=cc.acb_plot_type,
            markersize=cc.ac_signals_marker_size,
            marker=cc.ac_signal_marker,
            color=cc.ac_signal_sell_color,
        )
    
    return acs_plot

def make_ao_peak_above_plot(cc, plot_panel_id, data,ao_min):
    data.loc[:, AO_PEAK_ABOVE] = np.where(
            data[AO_PEAK_ABOVE] == 1.0, ao_min / 1.5, np.nan
        )
    aopabove_plot = mpf.make_addplot(
            data[AO_PEAK_ABOVE] - cc.ao_peak_offset_value,
            panel=plot_panel_id,
            type="scatter",
            markersize=cc.ao_peaks_marker_size,
            marker=cc.ao_peak_above_marker_higher,
            color=cc.aop_above_color,
        )
    
    return aopabove_plot

def make_ao_peak_bellow_plot(cc, plot_panel_id, data, ao_max):
    data.loc[:, AO_PEAK_BELLOW] = np.where(
            data[AO_PEAK_BELLOW] == 1.0, ao_max / 1.5, np.nan
        )
        # Make AO Peak Bellow plot

    aopbellow_plot = mpf.make_addplot(
            data[AO_PEAK_BELLOW] + cc.ao_peak_offset_value,
            panel=plot_panel_id,
            type="scatter",
            markersize=cc.ao_peaks_marker_size,
            marker=cc.ao_peak_bellow__marker_higher,
            color=cc.aop_bellow_color,
        )
    
    return aopbellow_plot

def ac_max_min(data):
    ac_max = data[AC].max()
    ac_min = data[AC].min()
    return ac_max,ac_min

def ao_max_min(data):
    ao_max = data[AO].max()
    ao_min = data[AO].min()
    return ao_max,ao_min

def save_add_figure(instrument:str, timeframe:str, rq:JGTADSRequest, fig:Figure):
    
    try:
            
        last_char_is_slash = rq.save_additional_figures_path[-1] == "/"
        is_an_image_path =False
        if len(rq.save_additional_figures_path) > 4:
            is_an_image_path = rq.save_additional_figures_path[-4] == "."
            #@STCIssue Directory must exist 24081921
            try: #Make directories where the image will be saved
                #Must extract the directory from the path (it has a filename)
                directory=ensure_directory_exists(rq.save_additional_figures_path)
                if not rq.quiet:
                    print("Directory created: " + directory)
            except Exception as e:
                print("Error creating directory for image: " + rq.save_additional_figures_path)
                print(e)
                #traceback.print_exc()
                

        # if rq.save_additional_figures_path is a filepath ,Save the figure
        if (
                os.path.isdir(rq.save_additional_figures_path) and not is_an_image_path
            ) or last_char_is_slash or rq.save_additional_figures_path == "pov":
            try:
                os.makedirs(rq.save_additional_figures_path, exist_ok=True)
            except:
                pass
            exn = ".png"
            
            
            path_part1 = rq.save_additional_figures_path
            if path_part1 == "pov" or rq.save_figure_as_pov:
                path_part1 = os.getcwd() #saving in current directory
            if rq.save_figure_as_timeframe:
                fn = timeframe + exn
            else:
                fn=instrument.replace("/", "-") + "_"  + timeframe  + exn
            final_figure_path = os.path.join(path_part1, fn)
            print("Saving figure to: " + final_figure_path)
            fig.savefig(
                final_figure_path,
                dpi=rq.save_additional_figures_dpi,
                )
        else:
            print("Saving figure to: " + rq.save_additional_figures_path)
            fig.savefig(
                    rq.save_additional_figures_path, dpi=rq.save_additional_figures_dpi
                )
    except Exception as e:
        print("Error saving figure to: " + rq.save_additional_figures_path)
        print(e)
        #traceback.print_exc()
        



def make_alligator_plots(
    plot_panel_id,
    data,
    cc:JGTChartConfig=None
):
    if cc is None:
        cc = JGTChartConfig()
    
    jaw_color = cc.jaw_color
    teeth_color = cc.teeth_color
    lips_color = cc.lips_color
    
    jaw_plot = mpf.make_addplot(
        data[JAW], panel=plot_panel_id, color=jaw_color
    )
    teeth_plot = mpf.make_addplot(
        data[TEETH], panel=plot_panel_id, color=teeth_color
    )
    lips_plot = mpf.make_addplot(
        data[LIPS], panel=plot_panel_id, color=lips_color
    )
    return jaw_plot, teeth_plot, lips_plot


# Too short plotting alternative


def plot_from_cds_df_ALT(
    data,
    instrument: str,
    timeframe: str,
    show: bool = True,
    cc: JGTChartConfig = None,
    rq: JGTADSRequest = None,
):
    """
    Plot OHLC bars, indicators, and signals from a pandas DataFrame.

    Args:
        data (pandas.DataFrame): The input DataFrame containing OHLC data.
        instrument (str): The instrument symbol.
        timeframe (str): The timeframe of the data.
        show (bool, optional): Whether to display the plot. Defaults to True.
        cc (JGTChartConfig, optional): The chart configuration object. Defaults to None.
        rq (JGTADSRequest, optional): The request object. Defaults to None.

    Returns:
        fig: The figure object of the plot.
        axes: The axes object of the plot.
    """
    if rq is not None:
        cc = rq.cc
    if cc is None:
        cc = JGTChartConfig()
    if rq is None:
        rq = JGTADSRequest(cc=cc)

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

    fig_ratio_x = cc.fig_ratio_x
    fig_ratio_y = cc.fig_ratio_y

    plot_style = cc.plot_style


    # plot config
    main_plot_panel_id = cc.main_plot_panel_id

    data_last_selection = data
    # Select the last 400 bars of the data
    tst_len_data = len(data)
    if nb_bar_on_chart != tst_len_data:
        data_last_selection = _select_charting_nb_bar_on_chart(data, nb_bar_on_chart)

    # Make OHLC bars plot
    ohlc = data_last_selection[[OPEN, HIGH, LOW, CLOSE]]

    # get date time of the last bar
    last_bar_dt = data_last_selection.index[-1]

    tittle_suffix = " " + str(len(data_last_selection)) + ""

    chart_title = instrument + " \n" + timeframe
    # + tittle_suffix + "  " + str(last_bar_dt)
    subtitle = (
        ""
        + get_dt_title_by_timeframe(last_bar_dt, timeframe)
        + "      "
        + tittle_suffix
    )

    fig, axes = mpf.plot(
        ohlc,
        type=cc.main_plot_type,
        style=plot_style,
        # addplot=addplot,
        volume=False,
        figratio=(fig_ratio_x, fig_ratio_y),
        title=chart_title,
        returnfig=True,
        tight_layout=True,
    )

    # Add subtitle to the first subplot
    axes[0].set_title(
        subtitle, fontsize=10, x=0.07, ha="left"
    )  # Add subtitle to the first subplot

    # Get current x-axis limits
    x_min, x_max = axes[main_plot_panel_id].get_xlim()

    # axe2ymin, axe2ymax = axes[ac_plot_panel_id].get_ylim()
    # l.debug("axe2ymin: " + str(axe2ymin))
    # l.debug("axe2ymax: " + str(axe2ymax))

    # Calculate new x-axis limit
    new_x_max = x_max + 8  # Add 8 for future bars

    # Set new x-axis limit
    axes[main_plot_panel_id].set_xlim(x_min, new_x_max)

    # Align the title to the left
    fig.suptitle(chart_title, x=0.05, ha="left")
    # fig.subtitle("oeuoeuoeu", x=0.15, ha="left")

    # Set the font size of the x-axis labels
    for ax in axes:
        ax.tick_params(axis="x", labelsize=6)

    # Set the font size of the Date column
    axes[main_plot_panel_id].tick_params(axis="x", labelsize=6)

    if rq.save_additional_figures_path is not None:
        save_add_figure(instrument, timeframe, rq, fig)
    
    if show:
        plt.show()
    return fig, axes, data_last_selection


def get_dt_title_by_timeframe(last_bar_dt, timeframe, separator="/"):
    format_str = {
        "M1": f"%y{separator}%m",  # Year-Month
        "W1": f"%y{separator}%m{separator}%d",  # Year-Week number
        "D1": f"%y{separator}%m{separator}%d",  # Year-Month-Day
        "H8": f"%y{separator}%m{separator}%d %H",  # Year-Month-Day Hour
        "H6": f"%y{separator}%m{separator}%d %H",  # Year-Month-Day Hour
        "H4": f"%y{separator}%m{separator}%d %H",  # Year-Month-Day Hour
        "H3": f"%y{separator}%m{separator}%d %H",  # Year-Month-Day Hour
        "H2": f"%y{separator}%m{separator}%d %H",  # Year-Month-Day Hour
        "H1": f"%y{separator}%m{separator}%d %H",  # Year-Month-Day Hour
        "m30": f"%y{separator}%m{separator}%d %H:%M",  # Year-Month-Day Hour:Minute
        "m15": f"%y{separator}%m{separator}%d %H:%M",  # Year-Month-Day Hour:Minute
        "m5": f"%y{separator}%m{separator}%d %H:%M",  # Year-Month-Day Hour:Minute
    }.get(
        timeframe, f"%Y{separator}%m{separator}%d %H:%M"
    )  # Default to full date-time if timeframe is not recognized

    return last_bar_dt.strftime(format_str)


def _select_charting_nb_bar_on_chart(data, nb_bar_on_chart):
    try:
        data_last_selection = data.iloc[-nb_bar_on_chart:].copy()
        # data_last_selection.to_csv("out_data_last_selection.csv")
    except:
        l.warning(
            "Could not select the desired amount of bars, trying anyway with what we have"
        )
        data_last_selection = data
        pass
    return data_last_selection


def make_plot__price_peaks__indicator(
    price_peak_above_color,
    price_peak_bellow_color,
    price_peak_marker_size,
    price_peak_above_marker,
    price_peak_bellow_marker,
    price_peak_above_coln,
    price_peak_bellow_coln,
    main_plot_panel_id,
    data_last_selection,
    price_peak_offset_value,
):
    price_peak_above_plot = mpf.make_addplot(
        data_last_selection[price_peak_above_coln] + price_peak_offset_value,
        panel=main_plot_panel_id,
        type="scatter",
        markersize=price_peak_marker_size,
        marker=price_peak_above_marker,
        color=price_peak_above_color,
    )
    price_peak_bellow_plot = mpf.make_addplot(
        data_last_selection[price_peak_bellow_coln] - price_peak_offset_value,
        panel=main_plot_panel_id,
        type="scatter",
        markersize=price_peak_marker_size,
        marker=price_peak_bellow_marker,
        color=price_peak_bellow_color,
    )
    return price_peak_above_plot, price_peak_bellow_plot


def make_plot_fractals_degreehigher_indicator(
    fractal_dn_color_higher,
    fractal_up_color_higher,
    fractal_degreehigher_marker_size,
    fractal_up_marker_higher,
    fractal_dn_marker_higher,
    fh_col_dim_higher,
    fl_col_dim_higher,
    main_plot_panel_id,
    data_last_selection,
    fractal_offset_value,
):
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

    return fractal_up_plot_higher, fractal_down_plot_higher




def make_plot_fractals_by_degree_UNIFIED(
    dn_color,
    up_color,
    marker_size,
    up_marker,
    dn_marker,
    plot_panel_id,
    data,
    fractal_offset_value=0,
    fractal_dim=8,
    plot_type = "scatter"
):
    fh_col_dim_higher = FH +  str(fractal_dim)
    fl_col_dim_higher = FL +  str(fractal_dim)
    
    up_plot = mpf.make_addplot(
        data[fh_col_dim_higher] + fractal_offset_value,
        panel=plot_panel_id,
        type=plot_type,
        markersize=marker_size,
        marker=up_marker,
        color=up_color,
    )
    down_plot = mpf.make_addplot(
        data[fl_col_dim_higher] - fractal_offset_value,
        panel=plot_panel_id,
        type=plot_type,
        markersize=marker_size,
        marker=dn_marker,
        color=dn_color,
    )

    return up_plot, down_plot




def make_plot__ac(
    data: pd.DataFrame, cc: JGTChartConfig = None, panel_plot_id=2,
    secondary_y = False
):
    if cc is None:
        cc = JGTChartConfig()

    colors_ac = [
        cc.ac_up_color if (data.iloc[i][AC] - data.iloc[i - 1][AC] > 0) else cc.ac_dn_color
        for i in range(1, len(data))
    ]
    colors_ac.insert(0, cc.ac_dn_color)

    ac_plot = mpf.make_addplot(
        data[AC],
        panel=panel_plot_id,
        color=colors_ac,
        secondary_y=secondary_y,
        type=cc.ac_plot_type,
        # label="AC"
    )

    return ac_plot


def make_plot__ao(
    data: pd.DataFrame, 
    cc: JGTChartConfig = None, 
    plot_panel_id=1,
    secondary_y = False
):
    if cc is None:
        cc = JGTChartConfig()


    # Calculate the color for 'ao' and 'ac' bar
    colors_ao = [
        (
            cc.ao_upbar_color
            if (data.iloc[i][AO] - data.iloc[i - 1][AO] > 0)
            else cc.ao_dnbar_color
        )
        for i in range(1, len(data[AO]))
    ]
    colors_ao.insert(0, cc.ao_dnbar_color)

    # Make 'ao' and 'ac' oscillator plot

    
    ao_plot = mpf.make_addplot(
        data[AO],
        panel=plot_panel_id,
        color=colors_ao,
        secondary_y=secondary_y,
        type=cc.ao_plot_type,
    )

    return ao_plot


def make_plot__fractals_indicator(
    fractal_up_color,
    fractal_dn_color,
    fractal_marker_size,
    fractal_up_marker,
    fractal_dn_marker,
    fh_col_dim,
    fl_col_dim,
    plot_panel_id,
    data,
    fractal_offset_value=0,
    fractals_plot_type="scatter",
):
    
    fractal_up_plot = mpf.make_addplot(
        data[fh_col_dim] + fractal_offset_value,
        panel=plot_panel_id,
        type=fractals_plot_type,
        markersize=fractal_marker_size,
        marker=fractal_up_marker,
        color=fractal_up_color,
    )
    fractal_down_plot = mpf.make_addplot(
        data[fl_col_dim] - fractal_offset_value,
        panel=plot_panel_id,
        type=fractals_plot_type,
        markersize=fractal_marker_size,
        marker=fractal_dn_marker,
        color=fractal_dn_color,
    )
    return fractal_up_plot, fractal_down_plot



def make_plot__fdb_signals(
    data,
    fdb_offset_value=0,
    plot_panel_id=0,
    cc: JGTChartConfig = None,
    fdb_plot_type="scatter",
):
    """
    Creates scatter plots for FDB buy and sell signals based on the given parameters.

    Args:
            plot_panel_id (int): ID of the main plot panel.
            data (pandas.DataFrame): Data containing the buy and sell signals.
            fdb_offset_value (float): Offset value to adjust the scatter plot positions.
            fdbs_plot_type (str, optional): Plot type for sell signals. Defaults to "scatter".

    Returns:
            tuple: A tuple containing the scatter plot for buy signals and the scatter plot for sell signals.
    """
    if cc is None:
        cc = JGTChartConfig()
    # Align fdbb with OHLC bars if value is '1.0'
    data.loc[:, FDBB] = np.where(
        data[FDB] == 1.0, data[HIGH], np.nan
    )
    data.loc[:, FDBS] = np.where(
        data[FDB] == -1.0, data[LOW], np.nan
    )
    fdbb_up_plot = make_plot_common_scatter_signal(
        data=data,
        tcol=FDBB,
        marker=cc.fdb_signal_marker,
        color=cc.fdb_signal_buy_color,
        marker_size=cc.fdb_marker_size,
        plot_panel_id=plot_panel_id,
        offset_value=fdb_offset_value,
        plot_type=fdb_plot_type,
    )
    
    fdbs_down_plot = make_plot_common_scatter_signal(
        data=data,
        tcol=FDBS,
        marker=cc.fdb_signal_marker,
        color=cc.fdb_signal_sell_color,
        marker_size=cc.fdb_marker_size,
        plot_panel_id=plot_panel_id,
        offset_value=fdb_offset_value,
        plot_type=fdb_plot_type,        
    )

    return fdbb_up_plot, fdbs_down_plot


def make_plot_common_scatter_signal(
    data,
    tcol,
    marker,
    color,
    marker_size=12,
    plot_panel_id=0,
    offset_value=0,
    plot_type="scatter",
):

    plot_result = mpf.make_addplot(
        data[tcol] - offset_value,
        panel=plot_panel_id,
        type=plot_type,
        markersize=marker_size,
        marker=marker,
        color=color,
    )

    return plot_result







def plot_perspective(rq: JGTADSRequest):
    rq.reset()
    # timeframes = rq.timeframes.split(",")
    perspective = {}
    perspective["rq"] = rq
    for tf in rq.timeframes:
        # instanciate a copy of the request
        _rq = rq.copy_with_timeframe(tf)
        _c, _a, _d = plot_v2(_rq, BETA_TRY=True)
        _p = {}
        _p = {"fig": _c, "axes": _a, "data": _d, "rq": _rq}
        perspective[tf] = _p
        # {"fig":_c,"axes":_a,"data":_d,"request":_rq}
    return perspective


def plot_v2(rq: JGTADSRequest, BETA_TRY=True):
    #rq.reset()
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


def plot(
    instrument: str = None,
    timeframe: str = None,
    show: bool = True,
    plot_ao_peaks: bool = True,
    cc: JGTChartConfig = None,
    tlid_range: str = None,
    crop_last_dt: str = None,
    use_fresh=False,
    rq: JGTADSRequest = None,
):
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
    if rq is not None:  # @STCIssue Transition to using just RQ
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

    fig, axes, cdfdata = jgtxplot18c_231209(
        instrument,
        timeframe,
        show=show,
        plot_ao_peaks=plot_ao_peaks,
        cc=cc,
        tlid_range=tlid_range,
        crop_last_dt=crop_last_dt,
        use_fresh=use_fresh,
        rq=rq,
    )

    return fig, axes, cdfdata



import argparse

def main():
    from jgtutils import jgtcommon
    from jgtpyconstants import ADSCLI_PROG_DESCRIPTION, ADSCLI_PROG_NAME, ADSCLI_PROG_EPILOG
    
    #print("JGTADS v0.1")
    # Parse arguments
    parser=jgtcommon.new_parser(ADSCLI_PROG_DESCRIPTION,ADSCLI_PROG_EPILOG,ADSCLI_PROG_NAME)

    parser=jgtcommon.add_instrument_timeframe_arguments(parser)
    
    # parser.add_argument("-i","--instrument", type=str, help="The name of the instrument.",required=True,metavar="instrument")
    # parser.add_argument("-t","--timeframe", type=str, help="The timeframe for the chart.",required=True,metavar="timeframe")
    
    #use fresh
    parser=jgtcommon.add_use_fresh_argument(parser)
    #parser.add_argument("-uf","--fresh", action="store_true", help="Whether to use fresh data.",default=False)
    #crop dt
    parser.add_argument("-dt","--crop_last_dt", type=str, help="The last date-time to crop the data.")
    parser.add_argument("--show", action="store_true", help="Whether to display the plot.",default=False)
    #save figure 
    parser.add_argument("-sf", "--save_figure", type=str, help="Save the figure to the given path.  Use t",default=None)
    #save_figure_as_pov_name flag
    parser.add_argument("-tf", "--save_figure_as_timeframe", action="store_true", help="Save the figure using just the timeframe as basename (ex. H4.png).",default=False)
    #save_figure_as_pov_name flag
    parser.add_argument("-pov", "--save_figure_as_pov_name", action="store_true", help="Save the figure as pov file.",default=False)
    #save dpi
    parser.add_argument("-dpi", "--save_additional_figures_dpi", type=int, help="The DPI of the saved figures.",default=300)
    
    parser=jgtcommon.add_verbose_argument(parser)
    #verbose level
    
    args=jgtcommon.parse_args(parser)
    if not args.show and args.save_figure is None and args.save_figure_as_pov_name is False:
        print("No output will be generated. Use -show or -sf to display or save the figure.")
        return

    # Create a JGTADSRequest object
    rq:JGTADSRequest = JGTADSRequest()
    rq.verbose_level = args.verbose

    # Set the instrument and timeframe
    rq.instrument = args.instrument
    rq.timeframe = args.timeframe
    
    #crop dt
    rq.crop_last_dt = args.crop_last_dt
    
    rq.use_fresh = args.fresh
    
    rq.show = args.show
        
    rq.save_additional_figures_dpi = args.save_additional_figures_dpi
    
    if args.save_figure is not None and (args.save_figure=='ct' or args.save_figure=='ctf'  or args.save_figure=='tc' or args.save_figure=='tcf' ):
        args.save_figure_as_timeframe=True
        args.save_figure="charts/"    
    elif args.save_figure is not None and (args.save_figure=='cpov' or args.save_figure=='cp' or args.save_figure=='cit' or args.save_figure=='itc'  or args.save_figure=='ic' or args.save_figure=='ci' ):
        args.save_figure_as_pov_name=True
        args.save_figure="charts/"    
    elif args.save_figure is not None and (args.save_figure=='t' or args.save_figure=='timeframe'  or args.save_figure=='tf'):
        args.save_figure_as_timeframe=True
        args.save_figure="."
    elif args.save_figure is not None and (args.save_figure=='pov' or args.save_figure=='it' or args.save_figure=='p' or args.save_figure=='i' ):
    
        args.save_figure_as_pov_name=True
        args.save_figure="."
    
    if  (args.save_figure_as_pov_name or args.save_figure_as_timeframe) and (args.save_figure is None or args.save_figure == "."):#if save_figure_as_pov_name is set and save_figure is not set
    
        rq.save_additional_figures_path = os.getcwd() #saving in current directory
    
    rq.save_figure_as_timeframe = args.save_figure_as_timeframe
    rq.save_figure_as_pov = args.save_figure_as_pov_name
    
    if args.save_figure is not None:
        rq.save_additional_figures_path = args.save_figure
    #print(args.save_figure)
    #print(rq.save_additional_figures_path)
    #exit()
    
        
    #many timeframs if , in the string timeframe
    if "," in rq.timeframe:
        timeframes = rq.timeframe.split(",")
    else:
        timeframes = [rq.timeframe]
    
    #foreach timeframes
    for tf in timeframes:
        rq.timeframe = tf
        # Plot the chart
        plot_v2(rq, BETA_TRY=True)

if __name__ == "__main__":
    main()
