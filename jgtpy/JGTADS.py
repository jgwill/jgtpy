#@title Plotly

import pandas as pd

import kaleido
import plotly

import jgtpy.JGTCDS as cds
import jgtpy.JGTConfig as jgtc

from matplotlib import pyplot as plt

import plotly.graph_objects as go
import plotly.subplots as sp


cdtformat="%Y-%m-%d"




from .jgtconstants import (
  sellingZoneColor,
  buyingZoneColor,
)

# %%
#@title INDICATOR's Data Frame Columns naming
# Import statements for jgtconstants.py variables


from .jgtconstants import (
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

from .jgtconstants import (
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

def pano_chart_pto221103(charts,_nbrows=3):
  panocharts = sp.make_subplots(rows=_nbrows, 
                                cols=1,
                                row_heights=[110.1.4,110],
                                shared_xaxes=True)
                                #column_widths=[75,75]
  cl=1
  r=1
  for c in charts:
    panocharts.add_trace(charts[c],row=r,col=cl)
    r=r+1
    # cl=cl+1
    # if cl==3:
    #   cl=1
  return panocharts
  







def update(_f4,_ch,_cw,showlegent=False,xaxis_rangeslider_visible=False):
  _f4.update_layout(height=_ch, width=_cw, 
                    showlegend=False, 
                    xaxis_rangeslider_visible=False)