
import pandas as pd
import datetime
from .JGTPDHelper import jgtpd_drop_col_by_name,ids_cleanse_ao_peak_secondary_columns,pds_cleanse_original_columns,pds_cleanse_extra_columns

from jgtapy import Indicators
import os

# %%
#@title Vars
_dtformat = '%m.%d.%Y %H:%M:%S'

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
    nonTradingZoneColor,
    sellingZoneColor,
    buyingZoneColor,
)

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















# %%
#@title Range shift add col drop na
#--@STCGoal PDS Utils
def _jgtpd_col_add_range_shifting_dropnas(dfsrc,ctxcolname=indicator_AO_awesomeOscillator_column_name,colprefix='pao',endrange=10):
  return _jgtpd_dropnas_on_any_rows(_jgtpd_col_add_range_shifting(dfsrc,ctxcolname,colprefix,endrange))

#@title BACKWARD Range shift col
def _jgtpd_col_add_range_shifting(dfsrc,ctxcolname=indicator_AO_awesomeOscillator_column_name,colprefix='pao',endrange=10):
  """Add a BACKWARD range of shifted values
    for a column with a prefixed numbered.

    Args:
         dfsrc (DataFrame source)
         ctxcolname (column name from)
         colprefix (new columns prefix)
         endrange (the end of the range from 0)
         
    Returns:
      DataFrame with new columns
  """
  for i in range(endrange):
    dfsrc[colprefix+str(i)]=dfsrc[ctxcolname].shift(i)
  return dfsrc

  
  
#@title Timeframe/Pov Utilities  (getMinByTF

def getMinByTF(tf):
  """
  Returns the number of minutes in the given timeframe string.

  Args:
  tf (str): timeframe string, one of 'm1', 'mi1', 'min1', 'm5', 'm15', 'm30', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H8', 'D1', 'W1', 'M1'

  Returns:
  int: number of minutes in the given timeframe string
  """
  if (tf=='m1' or tf=='mi1' or tf=='min1'): return 1
  if (tf=='m5' ): return 5
  if (tf=='m15' ): return 15
  if (tf=='m30' ): return 30
  if (tf=='H1' ): return 60
  if (tf=='H2' ): return 120
  if (tf=='H3' ): return 180
  if (tf=='H4' ): return 240
  if (tf=='H5' ): return 300
  if (tf=='H6' ): return 360
  if (tf=='H8' ): return 480
  if (tf=='D1' ): return 1440
  if (tf=='W1' ): return 10080
  if (tf=='M1' ): return 302400

  

#@title TODO Function to create adequate DateRange Request
import datetime

def pds_get_dt_from_and_to_for_now_live_price(_timeframe, _nbbar2retrieve=335, quiet=True):
  """
  Returns the start and end datetime strings for retrieving live price data.

  Args:
    _timeframe (int): The timeframe in minutes.
    _nbbar2retrieve (int, optional): The number of bars to retrieve. Defaults to 335.
    quiet (bool, optional): Whether to print weekday information. Defaults to True.

  Returns:
    tuple: A tuple containing the start and end datetime strings in the format '%m.%d.%Y %H:%M:%S'.
  """
  nbmintf = getMinByTF(_timeframe)
  now = datetime.datetime.now(datetime.timezone.utc)
  if not quiet:
    print('Now is: ' + str(now))
  weekdayoffset = 0
  chkweekday = now.weekday()
  if not quiet:
    print('Weekday is: ' + str(chkweekday))
  if chkweekday == 7:
    weekdayoffset = 1440
  if chkweekday == 0:
    weekdayoffset = 2840
  idsIndiPrepNbBars = 90
  dtminute = datetime.timedelta(minutes=nbmintf*(_nbbar2retrieve+weekdayoffset+idsIndiPrepNbBars))
  datefromobj = now - dtminute
  datefrom = datefromobj.strftime(_dtformat)
  nowstring = now.strftime(_dtformat)
  dateto = nowstring
  return datefrom, dateto


# %%
#--@STCGoal IDS Indicators and related / CDS



def ids_add_indicators(dfsrc,
                       enableGatorOscillator=False,
                       enableMFI=False,
                       dropnavalue=True,
                       quiet=False,                       
                       cleanupOriginalColumn=True,useLEGACY=True):
  """
  Adds technical indicators to a given DataFrame.

  Args:
  dfsrc (pandas.DataFrame): The DataFrame to which the indicators will be added.
  enableGatorOscillator (bool, optional): Whether to enable the Gator Oscillator indicator. Defaults to False.
  enableMFI (bool, optional): Whether to enable the Money Flow Index indicator. Defaults to False.
  dropnavalue (bool, optional): Whether to drop rows with NaN values. Defaults to True.
  quiet (bool, optional): Whether to suppress console output. Defaults to False.
  cleanupOriginalColumn (bool, optional): Whether to clean up the original column. Defaults to True.
  useLEGACY (bool, optional): Whether to use the legacy version of the function. Defaults to True.

  Returns:
  pandas.DataFrame: The DataFrame with the added indicators.
  """
  if not useLEGACY: # Because jgtapy has to be upgraded with new column name, we wont use it until our next release
    return Indicators.jgt_create_ids_indicators_as_dataframe(dfsrc,
                       enableGatorOscillator,
                       enableMFI,                          
                       cleanupOriginalColumn,                    
                       quiet)
  else:
    return ids_add_indicators_LEGACY(dfsrc,
                       enableGatorOscillator,
                       enableMFI,
                       dropnavalue,
                       quiet)

def ids_add_indicators_LEGACY(dfsrc,
                       enableGatorOscillator=False,
                       enableMFI=False,
                       dropnavalue=True,
                       quiet=False,
                       addAlligatorOffsetInFutur=True):
  """
  Adds various technical indicators to the input DataFrame. Is the same as in the jgtapy.legacy module.

  Args:
  dfsrc (pandas.DataFrame): The input DataFrame.
  enableGatorOscillator (bool, optional): Whether to enable the Gator Oscillator indicator. Defaults to False.
  enableMFI (bool, optional): Whether to enable the Money Flow Index indicator. Defaults to False.
  dropnavalue (bool, optional): Whether to drop rows with NaN values. Defaults to True.
  quiet (bool, optional): Whether to suppress print statements. Defaults to False.
  addAlligatorOffsetInFutur (bool, optional): (NOT IMPLEMENTED) Whether to add the Alligator offset in the future. Defaults to True.

  Returns:
  pandas.DataFrame: The input DataFrame with added technical indicators.
  """
  if not quiet:
    print("Adding indicators...")
  i=Indicators(dfsrc)
  
  i.accelerator_oscillator( column_name= indicator_AC_accelerationDeceleration_column_name)
  i.alligator(period_jaws=13, period_teeth=8, period_lips=5, shift_jaws=8, shift_teeth=5, shift_lips=3, column_name_jaws=indicator_currentDegree_alligator_jaw_column_name, column_name_teeth=indicator_currentDegree_alligator_teeth_column_name, column_name_lips=indicator_currentDegree_alligator_lips_column_name)
  i.alligator(period_jaws=89, period_teeth=55, period_lips=34, shift_jaws=55, shift_teeth=34, shift_lips=21, column_name_jaws=indicator_sixDegreeLarger_alligator_jaw_column_name, column_name_teeth=indicator_sixDegreeLarger_alligator_teeth_column_name, column_name_lips=indicator_sixDegreeLarger_alligator_lips_column_name)
  i.awesome_oscillator(column_name=indicator_AO_awesomeOscillator_column_name)
  
  # Creating Fractal Indicators for degrees 2,3,5,8,13,21,34,55,89 
  i.fractals(column_name_high=indicator_fractal_high_degree2_column_name, column_name_low=indicator_fractal_low_degree2_column_name)
  i.fractals3(column_name_high=indicator_fractal_high_degree3_column_name, column_name_low=indicator_fractal_low_degree3_column_name)
  i.fractals5(column_name_high=indicator_fractal_high_degree5_column_name, column_name_low=indicator_fractal_low_degree5_column_name)
  i.fractals8(column_name_high=indicator_fractal_high_degree8_column_name, column_name_low=indicator_fractal_low_degree8_column_name)
  i.fractals13(column_name_high=indicator_fractal_high_degree13_column_name, column_name_low=indicator_fractal_low_degree13_column_name)
  i.fractals21(column_name_high=indicator_fractal_high_degree21_column_name, column_name_low=indicator_fractal_low_degree21_column_name)
  i.fractals34(column_name_high=indicator_fractal_high_degree34_column_name, column_name_low=indicator_fractal_low_degree34_column_name)
  i.fractals55(column_name_high=indicator_fractal_high_degree55_column_name, column_name_low=indicator_fractal_low_degree55_column_name)
  i.fractals89(column_name_high=indicator_fractal_high_degree89_column_name, column_name_low=indicator_fractal_low_degree89_column_name)

  
  if enableGatorOscillator:
    
    i.gator(period_jaws=13, period_teeth=8, period_lips=5, shift_jaws=8, shift_teeth=5, shift_lips=3, column_name_val1=indicator_gatorOscillator_low_column_name, column_name_val2=indicator_gatorOscillator_high_column_name)

  if enableMFI:
    i.bw_mfi(column_name=indicator_mfi_marketFacilitationIndex_column_name)
  
  if addAlligatorOffsetInFutur:
    _add_alligator_tmpcol_offset_in_futur(i)
  
  dfresult = i.df


  if dropnavalue:
    dfresult = dfresult.dropna()
  try: 
    dfresult = dfresult.set_index('Date')
  except TypeError:
    pass
  if not quiet:
    print("done adding indicators :)")
  
  # if addAlligatorOffsetInFutur:
  #   _offset_alligator_tmpcol_in_futur(dfresult)
  return dfresult

def _offset_alligator_tmpcol_in_futur(dfsrc):
  dfsrc['jaws_tmp2'] = dfsrc['jaws_tmp'].shift(8)
  dfsrc['teeth_tmp2'] = dfsrc['teeth_tmp'].shift(5)
  dfsrc['lips_tmp2'] = dfsrc['lips_tmp'].shift(3)
  
  return dfsrc


def _add_alligator_tmpcol_offset_in_futur(i):
  
  i.smma( 8, 'jaws_tmp', 'Median')
  i.smma( 5, 'teeth_tmp', 'Median')
  i.smma( 3, 'lips_tmp', 'Median')
  #df=i.df
  # Define the logic for adding alligator offset in the future
  # ...
  #indicator_currentDegree_alligator_jaw_column_name
  # from jgtapy.utils import  calculate_smma
  # df_j = calculate_smma(df['Median'], 8, 'jaws_tmp', median_col)
  # df_t = calculate_smma(df_median, period_teeth, column_name_teeth, median_col)
  # df_l = calculate_smma(df_median, period_lips, column_name_lips, median_col)

  # # Shift SMMAs
  # df_j[column_name_jaws] = df_j[column_name_jaws].shift(shift_jaws)
  # df_t[column_name_teeth] = df_t[column_name_teeth].shift(shift_teeth)
  # df_l[column_name_lips] = df_l[column_name_lips].shift(shift_lips)

  return i

# %%
#@title Pandas JGT Utilities

def _jgtpd_dropnas_on_any_rows(dfsrc):
	return dfsrc.dropna(axis='rows')
	
def _jgtpd_drop_cols_from_to_by_name(dfsrc,firstcolname,lastcolname,_axis = 1):
  return dfsrc.drop(dfsrc.loc[:, firstcolname:lastcolname].columns,axis = _axis)


def _jgtpd_col_drop_range(dfsrc,colprefix='pao',endrange=10):
	_firstcolname=colprefix+str(1)
	_lastcolname=colprefix+str(endrange)
	return _jgtpd_drop_cols_from_to_by_name(dfsrc,_firstcolname,_lastcolname,1)



def _ids_add_fdb_intermediaries_columns(dfsrc):
  """
  Adds intermediate columns to the given DataFrame for the purpose of
  identifying fractal bullish and bearish bars.

  Args:
  - dfsrc: A pandas DataFrame containing OHLC data.

  Returns:
  - A pandas DataFrame with additional columns for intermediate calculations.
  """
  
  #Bullish
  dfsrc['HighisBellowLips'] = dfsrc.lips > dfsrc.High

  dfsrc['LowIsLower']= dfsrc.Low < dfsrc.Low.shift()

  dfsrc['ClosedAboveMedian'] = dfsrc.Close > dfsrc.Median

  #Bearish

  dfsrc['LowisAboveLips'] = dfsrc.lips < dfsrc.Low

  dfsrc['HighIsHigher']= dfsrc.High > dfsrc.High.shift()

  dfsrc['ClosedBellowMedian'] = dfsrc.Close < dfsrc.Median
  return dfsrc


def _ids_clear_fdb_intermediaries_columns(dfsrc,quiet=False):
  """
  This function drops FDB columns from a pandas dataframe that are not needed for further processing.
  
  Args:
  - dfsrc: pandas dataframe
  - quiet: boolean, default False. If True, suppresses the print statement when KeyError is caught.
  
  Returns:
  - dfsrc: pandas dataframe with the specified columns dropped.
  """
  try:
    dfsrc =_jgtpd_drop_cols_from_to_by_name(dfsrc,
          'HighisBellowLips',
        'ClosedBellowMedian')
  except KeyError:
    if not quiet:
      print("Might cleared already")
    pass
  return dfsrc



#@title FDB Bullish logics
#from : https://stackoverflow.com/questions/23330654/update-a-dataframe-in-pandas-while-iterating-row-by-row

def _ids_add_fdb_column_logics(dfsrc,
                              _dropIntermediariesColumns=True,
                              quiet=False):
  """
  Adds FDB (Fractal Divergence Buy) and FDS (Fractal Divergence Sell) columns to the input dataframe based on certain conditions.
  
  Args:
  - dfsrc: pandas dataframe, input dataframe to which FDB and FDS columns need to be added.
  - _dropIntermediariesColumns: bool, default True. If True, intermediary columns added during the calculation will be dropped.
  - quiet: bool, default False. If True, suppresses the print statements.

  Returns:
  - dfsrc: pandas dataframe, dataframe with FDB and FDS columns added.
  """
  dfsrc=_ids_add_fdb_intermediaries_columns(dfsrc)
  for i, row in dfsrc.iterrows():

      ClosedAboveMedian = dfsrc.at[i,'ClosedAboveMedian']
      LowIsLower = dfsrc.at[i,'LowIsLower']
      HighisBellowLips  = dfsrc.at[i,'HighisBellowLips']
      ClosedBellowMedian = dfsrc.at[i,'ClosedBellowMedian']
      HighIsHigher = dfsrc.at[i,'HighIsHigher']
      LowisAboveLips  = dfsrc.at[i,'LowisAboveLips']

      #default values 
      dfsrc.at[i, signalBuy_fractalDivergentBar_column_name] = 0
      dfsrc.at[i, signalSell_fractalDivergentBar_column_name] = 0
      dfsrc.at[i,signalCode_fractalDivergentBar_column_name] = 0 

      ##################################################
      #########   FDBB
      isFDB = 0
      isFDBCode = 0
      high=0
      low=0
      if HighisBellowLips and LowIsLower and ClosedAboveMedian   :
          isFDB = 1
          isFDBCode = 1
          high  = dfsrc.at[i,'High']
          low  = dfsrc.at[i,'Low']
      dfsrc.at[i,'fdbbhigh'] = high 
      dfsrc.at[i,'fdbblow'] = low 
      
      dfsrc.at[i,signalBuy_fractalDivergentBar_column_name] = isFDB  
      dfsrc.at[i,signalCode_fractalDivergentBar_column_name] = isFDBCode   # So we have All
      isAfdbb = isFDB
      ##################################################
      #########   FDBS
      
      if not isAfdbb:
        isFDB = 0    
        isFDBCode = 0
        high=0
        low=0
        if LowisAboveLips and HighIsHigher and ClosedBellowMedian   :
            isFDB = 1
            isFDBCode = -1
            high  = dfsrc.at[i,'High']
            low  = dfsrc.at[i,'Low']
            
        dfsrc.at[i,'fdbshigh'] = high 
        dfsrc.at[i,'fdbslow'] = low 
        
        dfsrc.at[i,signalSell_fractalDivergentBar_column_name] = isFDB
        dfsrc.at[i,signalCode_fractalDivergentBar_column_name] = isFDBCode
  if _dropIntermediariesColumns:
    dfsrc = _ids_clear_fdb_intermediaries_columns(dfsrc,quiet=quiet)
  return dfsrc








#@title AOF function pto (AO Fractals)



#@title Range shift col
def jgtids_mk_ao_fractal_peak(dfsrc,
                              ctxcolname=indicator_AO_awesomeOscillator_column_name,
                              poscolprefix='pao',
                              negcolprefix='nao',
                              endrange=10,
                              quiet=False):
  """ Make the AO Fractal Peak

    Args:
         dfsrc (DataFrame source)
         ctxcolname (column name from)
         poscolprefix (prefix positive (futur) ao sec col )
         negcolprefix (prefix negative (past) ao sec col )          
         endrange (total range from 0 (zero being the current in the output))
         
    Returns:
      DataFrame with new AO Peak columns 
        aof (21,13,0,-13,-21) Fractal value of the peak
        aofvalue (AO Value)
        aofhighao (AO value on Bullish Peak)
        aoflowao (AO value of Bearish Peak)
        aofhigh  (Price High of that peak)
        aoflow   (Price Low of that Peak)

  """

  half = endrange/2
  l_df=len(dfsrc)
  for o in range(endrange):   
    i=int(o-half)
    
    _cn=poscolprefix+str(i)
    if i < 0:
      _cn=negcolprefix+str(i).replace('-','')
    dfsrc[_cn]=dfsrc[ctxcolname].shift(i)
   

  # This filters out some noisy peaks that are too low or too high
  df_standardDeviation = dfsrc[ctxcolname].std()
  df_max = dfsrc[ctxcolname].max()
  df_min = dfsrc[ctxcolname].min()
  df_filterOutAOFThreshold_ABOVE = (df_standardDeviation + df_max) / 2
  df_filterOutAOFThreshold_BELLOW = ((df_standardDeviation * -1) + df_min) / 2
  
  if not quiet:
    print("filterout (std) Above(max)/(min)Bellow:  ("+ str(df_standardDeviation) + ")  " + str(df_filterOutAOFThreshold_ABOVE) + "(" + str(df_max) + ") / (" + str(df_min) + ") " + str(df_filterOutAOFThreshold_BELLOW))
  
  # Counting the peaks
  countUpPeak=0
  countDownPeak=0
  countDiscarted=0
  for i,row in dfsrc.iterrows():
    barAOF = 0
    dt=i
    curHigh= dfsrc.at[i,'High']
    curLow= dfsrc.at[i,'Low']
    cur=dfsrc.at[i,indicator_AO_awesomeOscillator_column_name]
    n9= dfsrc.at[i,'n9']
    n13= dfsrc.at[i,'n13']
    n12= dfsrc.at[i,'n12']
    n11= dfsrc.at[i,'n11']
    n10= dfsrc.at[i,'n10']
    n8= dfsrc.at[i,'n8']
    n7= dfsrc.at[i,'n7']
    n6= dfsrc.at[i,'n6']
    n5= dfsrc.at[i,'n5']
    n4= dfsrc.at[i,'n4']
    n3= dfsrc.at[i,'n3']
    n2= dfsrc.at[i,'n2']
    n1= dfsrc.at[i,'n1']
    p0= dfsrc.at[i,'p0']
    p1= dfsrc.at[i,'p1']
    p2= dfsrc.at[i,'p2']
    p3= dfsrc.at[i,'p3']
    p4= dfsrc.at[i,'p4']
    p5= dfsrc.at[i,'p5']
    p6= dfsrc.at[i,'p6']
    p7= dfsrc.at[i,'p7']
    p8= dfsrc.at[i,'p8']
    p9= dfsrc.at[i,'p9']
    p10= dfsrc.at[i,'p10']
    p11= dfsrc.at[i,'p11']
    p12= dfsrc.at[i,'p12']
    p13= dfsrc.at[i,'p13']

    outHigh=0
    outHighAO=0
    outLow=0
    outLowAO=0
    
    # Ways to find a peak that might be enhanced later with another methods using sequence recognition in machine learning
    if (
        (cur > p1 and cur > p2 and cur > p3 and cur > p4 
         and  
         cur > p5 and cur > p6 and cur > p7 and cur > p8
         and
         cur > p8 and cur > p9 and cur > p10 and cur > p11 
         and cur > p12 and cur > p13
         ) 
          and   
        (cur > n1 and cur > n2 and cur > n3 and cur > n4 
         and
         cur > n5 and cur > n6 and cur > n7 and cur > n8 
         and
         cur > n9 and cur > n10 and cur > n11 and cur > n12 and cur > n13
         )
        ):
      if cur > 0 and cur > df_filterOutAOFThreshold_ABOVE:
        barAOF=21        
        if not quiet:
          print("We have an up peak at:" + str(dt))
        countUpPeak=countUpPeak+1
      else:
        if cur >0 and cur > df_standardDeviation and barAOF != 21:
          barAOF = 13
          if not quiet:     
            print("We have an up peak at:" + str(dt))
          countUpPeak=countUpPeak+1
    else:
      if (
        (cur < p1 and cur < p2 and cur < p3 and cur < p4 
         and  
         cur < p5 and cur < p6 and cur < p7 and cur < p8
         and
         cur < p8 and cur < p9 and cur < p10 and cur < p11 
         and cur < p12 and cur < p13
         ) 
          and   
        (cur < n1 and cur < n2 and cur < n3 and cur < n4 
         and
         cur < n5 and cur < n6 and cur < n7 and cur < n8 
         and
         cur < n9 and cur < n10 and cur < n11 and cur < n12 and cur < n13
         )
        ): 
        if cur < 0 and cur < df_filterOutAOFThreshold_BELLOW:
          barAOF=-21          
          if not quiet:
            print("We have an down peak at: " + str(dt))
          countDownPeak=countDownPeak+1
        else :
          if cur < 0 and cur < df_standardDeviation*-1 and barAOF != -21:
            barAOF = -13
            if not quiet:
              print("We have an down peak at: " + str(dt))
            countDownPeak=countDownPeak+1
    if barAOF != 0:
      if cur > 0:
        outHigh=curHigh
        outHighAO=cur
        outLowAO=0
        outLow=0 # We are Above ZL so we dont want to use Low
      else:
        outHigh=0 # We are Bellow ZL so we dont want to use High
        outLow=curLow
        outLowAO=cur
        outHighAO=0
    
    # AOF is the Fractal Peak Value, it would be used to find twin peak signals and learn 
    
    #@STCIssue I question the use of some of these columns, they might be temporary 
    
    dfsrc.at[i,indicator_ao_fractalPeakOfMomentum_column_name]=barAOF
    dfsrc.at[i,indicator_ao_fractalPeakValue_column_name]=cur #current AO Value
    dfsrc.at[i,'aofhighao']=outHighAO  
    dfsrc.at[i,'aoflowao']=outLowAO  
    dfsrc.at[i,'aofhigh']=outHigh  
    dfsrc.at[i,'aoflow']=outLow 
  l_df = len(dfsrc)
  if not quiet:
    print("Total Peak - Up:" + str(countUpPeak) + ", Dn: " + str(countDownPeak) + " on total: " + str(l_df))
  dfsrc=ids_cleanse_ao_peak_secondary_columns(dfsrc,True)
  return dfsrc












#@title Add CDS signals

def cds_add_signals_to_indicators(dfires,_aopeak_range=28,quiet=False):
  dfires=_ids_add_fdb_column_logics(dfires,quiet=quiet)
  dfires = jgtids_mk_ao_fractal_peak(dfires,
                                   indicator_AO_awesomeOscillator_column_name,
                                   'p',
                                   'n',
                                   _aopeak_range,
                                   quiet=quiet)
  return dfires



def tocds(dfsrc,quiet=True):
  dfires = ids_add_indicators(dfsrc,quiet=quiet)
  dfires = cds_add_signals_to_indicators(dfires,quiet=quiet)
  dfires = jgti_add_zlc_plus_other_AO_signal(dfires,quiet=quiet)
  dfires = pds_cleanse_original_columns(dfires,quiet=True)
  dfires = ids_cleanse_ao_peak_secondary_columns(dfires,quiet=True)
  dfires = __format_boolean_columns_to_int(dfires,quiet=True)
  return dfires


def __format_boolean_columns_to_int(dfsrc, quiet=True):
  for col in dfsrc.columns:
    if dfsrc[col].dtype == bool:
      dfsrc[col] = dfsrc[col].astype(int)
  return dfsrc
  









#@title PD Columen Cleanup Functions

# def jgtpd_drop_col_by_name(dfsrc,colname,axis = 1,quiet=False):
#   """Drop Column in DF by Name

#   Args:
#         dfsrc (DataFrame source)
#         ctxcolname (column name from)
#         axis (  axis)
#         quiet (quiet output)
        
#   Returns:
#     Clean DataFrame 
#   """
#   if colname in dfsrc.columns:
#     return dfsrc.drop(dfsrc.loc[:, colname:colname].columns,axis = axis)
#   else:
#     # if not quiet:
#     #   print('Col:' + colname + ' was not there')
#     return dfsrc








  
#@title ZLC Buy and Sell v2 2210161707 

def jgti_add_zlc_plus_other_AO_signal(dfsrc,dropsecondaries=True,quiet=True):
  dfsrc=_jgtpd_col_add_range_shifting(dfsrc,indicator_AO_awesomeOscillator_column_name,'pao',10)
  dfsrc=_jgtpd_col_add_range_shifting(dfsrc,indicator_AC_accelerationDeceleration_column_name,'pac',4)
  if not quiet:
    print('----added shofted range AO')

  # AO Above Zero
  dfsrc[indicator_AO_aboveZero_column_name]= (dfsrc[indicator_AO_awesomeOscillator_column_name]>0 ).astype(int) 
  # AO Bellow Zero
  dfsrc[indicator_AO_bellowZero_column_name]= (dfsrc[indicator_AO_awesomeOscillator_column_name] < 0).astype(int) 
  
  c=0
  xc=len(dfsrc)
  for i,row in dfsrc.iterrows():
    c=c+1
    cao=dfsrc.at[i,indicator_AO_awesomeOscillator_column_name] # Current AO
    cac=dfsrc.at[i,indicator_AC_accelerationDeceleration_column_name] # Current AC
    pac1=dfsrc.at[i,'pac1'] # Past AC 1
    pac2=dfsrc.at[i,'pac2'] # Past AC 2
    pac3=dfsrc.at[i,'pac3'] # Past AC 3
    cacgreen = False
    pac1green=False
    pac2green=False
    if cac > pac1:
      cacgreen=True
    if pac1 > pac2:
      pac1green=True
    if pac2 > pac3:
      pac2green=True
    
    pao1=dfsrc.at[i,'pao1'] # Past AO 1
    pao2=dfsrc.at[i,'pao2'] # Past AO 2
    pao3=dfsrc.at[i,'pao3'] # Past AO 3
    caogreen = False
    pao1green=False
    pao2green=False
    if cao > pao1:
      caogreen=True
    if pao1 > pao2:
      pao1green=True
    if pao2 > pao3:
      pao2green=True
    
    # For simplicity
    caored= not caogreen
    pao1red= not pao1green
    pao2red= not pao2green
    
    cacred= not cacgreen
    pac1red= not pac1green
    pac2red= not pac2green
    
    
    aoaz=dfsrc.at[i,indicator_AO_aboveZero_column_name]
    aobz=dfsrc.at[i,indicator_AO_bellowZero_column_name]

    #ZLC
    isZLCBuy = 0
    isZLCSell = 0
    zlcCode=0
    if pao1 > 0 and aobz == 1:
      zlcCode = -1
      isZLCSell=1
    if pao1 < 0 and aoaz == 1:
      zlcCode = 1
      isZLCBuy=1
    
    
    
    dfsrc.at[i,indicator_zeroLineCross_column_name] = zlcCode  
    dfsrc.at[i,signalBuy_zeroLineCrossing_column_name] = isZLCBuy
    dfsrc.at[i,signalSell_zeroLineCrossing_column_name] = isZLCSell

    #Coloring AO
    if caogreen:
      dfsrc.at[i,'aocolor'] = 'rgb(0,255,0)'
    else:
      dfsrc.at[i,'aocolor'] = 'rgb(255,0,0)'
      
    #Coloring AC
    if cacgreen:
      dfsrc.at[i,'accolor'] = 'rgb(0,255,0)'
    else:
      dfsrc.at[i,'accolor'] = 'rgb(255,0,0)'
      
    
    # --@STCIssue Zone  (Not sure, it might have to be ABove or Bellow)

    zoneColor = nonTradingZoneColor                #default Zone Color
    
    redZone = 0
    if cacred and caored and pac1red and pao1red:
      redZone=1
      zoneColor = sellingZoneColor

    greenZone = 0
    if cacgreen and caogreen and pac1green and pao1green:
      greenZone=1
      zoneColor=buyingZoneColor
      
    dfsrc.at[i,signal_zcol_column_name] = zoneColor
    
    #Sell Zone Signal
   
    dfsrc.at[i,signalSell_zoneSignal_column_name]= redZone
    
    #Buy Zone Signal
    dfsrc.at[i, signalBuy_zoneSinal_column_name] = greenZone
    
    #AC Sell / Buy  3 AC Against AO af AC Bellow, 2 if above
    acSell = 0
    msgacSignal = "No "
    if cacred and pac1red and caogreen and pao1green:
      acSell=1      
      if cac < 0 and pac2green:# We require 3 bars red on the AC When bellow zero
        acSell=0
    acBuy = 0
    if cacgreen and pac1green and caored and pao1red:
      acBuy=1
      if cac>0 and pac2red:        
        acBuy=0
    
    #AC Sell Signal (Deceleration)
    
    dfsrc.at[i, signalSell_AC_deceleration_column_name] = acSell
    
    #AC Buy Signal (Acceleration)
    dfsrc.at[i,signalBuy_AC_acceleration_column_name]=acBuy
    
    if acSell and not quiet:
      print("AC Sell Signal with AC Bellow Zero Line "+ str(i))
    if acBuy and not quiet:
      print("AC Buy Signal with AC ABove Zero Line "+ str(i))
    
    #Saucer Strategy
    # More on Saucer Strategy : http://simp.ly/p/2K1HBr
    saucerSell=0
    if cao < 0 and caored and pao1green and pao2green :
      saucerSell=1
      
    saucerBuy=0
    if cao > 0 and caogreen and pao1red and pao2red:
      saucerBuy=1
    
    dfsrc.at[i,signalSell_saucer_column_name]=saucerSell
    dfsrc.at[i,signalBuy_saucer_column_name]=saucerBuy
    
    # What Happens on the Next PLUS 35 Periods ??
    if c < xc - 35:
      cPrice = row['Close']
    # What Happens on the Next PLUS 55 Periods ??
  return dfsrc
    