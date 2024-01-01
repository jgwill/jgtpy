with this plotting function, create a class in which each made subplot (   jaw_plot,
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
        acb_plot) will be returned in an appropriate object we can reuse when we desire to plot these parts in other charting experiments


```python


def plot_from_cds_df(data,instrument,timeframe,nb_bar_on_chart = -1,show=True,plot_ao_peaks=True,cc: JGTChartConfig=None):
    
    """
    Plot OHLC bars, indicators, and signals from a pandas DataFrame.

    Args:
        data (pandas.DataFrame): The input DataFrame containing OHLC data.
        instrument (str): The instrument symbol.
        timeframe (str): The timeframe of the data.
        nb_bar_on_chart (int, optional): The number of bars to display on the chart. Defaults to 375.
        show (bool, optional): Whether to display the plot. Defaults to True.
        plot_ao_peaks (bool, optional): Whether to plot AO peaks. Defaults to False.
        cc (JGTChartConfig, optional): The chart configuration object. Defaults to None.

    Returns:
        fig: The figure object of the plot.
        axes: The axes object of the plot.
    """
    if cc is None:
        cc= JGTChartConfig()
    if nb_bar_on_chart==-1:
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
    
    if nb_bar_on_chart==-1:
        nb_bar_on_chart = cc.nb_bar_on_chart
        
    
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
    main_plot_panel_id=0
    ao_plot_panel_id=1
    ac_plot_panel_id=2
    
    
    
    #%% Select the last 400 bars of the data
    
    # Select the last 400 bars of the data
    try:
        data_last_selection = data.iloc[-nb_bar_on_chart:].copy()
        #data_last_selection.to_csv("out_data_last_selection.csv")
    except:
        l.warning("Could not select the desired amount of bars, trying anyway with what we have")
        data_last_selection = data
        pass
    
    # Make OHLC bars plot
    ohlc = data_last_selection[[OPEN, HIGH, LOW, CLOSE]]
    
    
    
    
    
    #%% AO/AC
    # AO / AC
    ao_plot,ac_plot = create_ao_ac_plots(data_last_selection,cc)
    
    
    # @STCGoal Make AO/AC signals plotted
    
    
    
    #%% Alligator
    
    #@STCIssue no offset data in, not offset columns: jaws_tmp,teeth_tmp,lips_tmp
    
    # Make Alligator's lines plot
    
    jaw_plot = mpf.make_addplot(data_last_selection[JAW], panel=main_plot_panel_id, color=jaw_color)
    teeth_plot = mpf.make_addplot(data_last_selection[TEETH], panel=main_plot_panel_id, color=teeth_color)
    lips_plot = mpf.make_addplot(data_last_selection[LIPS], panel=main_plot_panel_id, color=lips_color)
    
    
    #%% Offsets and various values
    # offset
    
    min_timeframe = getMinByTF(timeframe)
    price_mean = data_last_selection[CLOSE].mean()
    
    # Calculate the bar height for each row
    data_last_selection[BAR_HEIGHT] = data_last_selection[HIGH] - data_last_selection[LOW]
    
    
    # Calculate the average bar height
    average_bar_height = data_last_selection[BAR_HEIGHT].mean()
    low_min = data_last_selection[LOW].min()
    high_max = data_last_selection[HIGH].max()
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
        AO_PEAK_BELLOW = c.AO_PEAK_BELLOW#'ao_peak_bellow'
        AO_PEAK_ABOVE = c.AO_PEAK_ABOVE#'ao_peak_above'
        
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
    
    
    # Align saucer with OHLC bars if value is '1.0'
    data_last_selection.loc[:,ACB] = np.where(
        data_last_selection[ACB] == 1.0, data_last_selection[AC], np.nan
    )
    data_last_selection.loc[:,ACS] = np.where(
        data_last_selection[ACS] == 1.0, data_last_selection[AC], np.nan
    )

    sig_ac_offset_value = 0


    # Make Buy Signal plot
    acb_plot = mpf.make_addplot(
        data_last_selection[ACB] + sig_ac_offset_value,
        panel=ac_plot_panel_id,
        type="scatter",
        markersize=ac_signals_marker_size,
        marker=ac_signal_marker,
        color=ac_signal_buy_color,
    )
    # Make Sell Signal plot
    acs_plot = mpf.make_addplot(
        data_last_selection[ACS] - sig_ac_offset_value,
        panel=ac_plot_panel_id,
        type="scatter",
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
        addplot.append(price_peak_above_plot)
        addplot.append(price_peak_bellow_plot)


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
    main_ymax, main_ymin = axes[main_plot_panel_id].get_ylim()
    height_minmax = main_ymax - main_ymin
    tst_v = height_minmax / 8
    new_y_max = main_ymin - tst_v - fdb_offset_value
    new_y_min = main_ymax + tst_v + fdb_offset_value
    #print("mainYMin/low/newmin: " + str(main_ymin) + " / " + str(low_min) + " / " + str(new_y_min))
    #print("mainYMax/high/newmax :"  +str(main_ymax) + " / " + str(high_max) + " / " + str(new_y_max))
    axes[main_plot_panel_id].set_ylim(
        new_y_min,
        new_y_max
    )
        
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
    fig.suptitle(instrument + "  " + timeframe, x=0.05, ha="left")

    # Set the font size of the x-axis labels
    for ax in axes:
        ax.tick_params(axis="x", labelsize=6)

    # Set the font size of the Date column
    axes[main_plot_panel_id].tick_params(axis="x", labelsize=6)

    if show:
        plt.show()
    return fig,axes



```