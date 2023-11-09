"""
This module contains various utility functions for working with financial data and indicators. Mostly they are used by CDS

Functions:
- jgtpd_col_add_range_shifting_dropnas(_df,ctxcolname='ao',colprefix='pao',endrange=10)
- jgtpd_col_add_range_shifting(_df,ctxcolname='ao',colprefix='pao',endrange=10)
- getMinByTF(tf)
- pds_get_dt_from_and_to_for_now_live_price(_timeframe,_nbbar2retrieve=335,quiet=True)
- ids_add_indicators(__df,enableGatorOscillator=False,enableMFI=False,dropnavalue=True,quiet=False,cleanupOriginalColumn=True)
- ids_add_indicators_LEGACY(__df,enableGatorOscillator=False,enableMFI=False,dropnavalue=True,quiet=False)
- jgtpd_dropnas_on_any_rows(_df)
- jgtpd_drop_cols_from_to_by_name(_df,firstcolname,lastcolname,_axis = 1)
- jgtpd_col_drop_range(_df,colprefix='pao',endrange=10)
- ids_add_fdb_intermediaries_columns(_df)
- ids_clear_fdb_intermediaries_columns(_df,quiet=False)
- ids_add_fdb_column_logics(_df,_dropIntermediariesColumns=True,quiet=False)
- jgtids_mk_ao_fractal_peak(_df,ctxcolname='ao',poscolprefix='pao',negcolprefix='nao',endrange=10,quiet=False)

"""
# %%
#@title FDB Intermediary values
#@title Add Indicators Columns
import pandas as pd
import datetime
from jgtapy import Indicators

# %%
#@title Vars
_dtformat = '%m.%d.%Y %H:%M:%S'

# %%
#@title Data Frame Columns naming
indicator_currentDegree_alligator_jaw_column_name = 'jaw' # 13 periods moving average, shifted 8 bars into the future
indicator_currentDegree_alligator_teeth_column_name = 'teeth' # 8 periods moving average, shifted 5 bars into the future
indicator_currentDegree_alligator_lips_column_name = 'lips' # 5 periods moving average, shifted 3 bars into the future
indicator_sixDegreeLarger_alligator_jaw_column_name = 'bjaw' # 89 periods moving average, shifted 55 bars into the future
indicator_sixDegreeLarger_alligator_teeth_column_name = 'bteeth' # 55 periods moving average, shifted 34 bars into the future
indicator_sixDegreeLarger_alligator_lips_column_name = 'blips' # 34 periods moving average, shifted 21 bars into the future
indicator_AO_awesomeOscillator_column_name = 'ao' # AO measure energy of momentum
indicator_AC_accelerationDeceleration_column_name = 'ac' # AC measure speed of momentum
indicator_fractal_high_degree2_column_name = 'fb'
indicator_fractal_low_degree2_column_name = 'fs' 

#generated
indicator_fractal_high_degree2_column_name="fh" # Fractal High of degree 2
indicator_fractal_low_degree2_column_name="fl" # Fractal Low of degree 2
indicator_fractal_high_degree3_column_name="fh3" # Fractal High of degree 3
indicator_fractal_low_degree3_column_name="fl3" # Fractal Low of degree 3
indicator_fractal_high_degree5_column_name="fh5" # Fractal High of degree 5
indicator_fractal_low_degree5_column_name="fl5" # Fractal Low of degree 5
indicator_fractal_high_degree8_column_name="fh8" # Fractal High of degree 8
indicator_fractal_low_degree8_column_name="fl8" # Fractal Low of degree 8
indicator_fractal_high_degree13_column_name="fh13" # Fractal High of degree 13
indicator_fractal_low_degree13_column_name="fl13" # Fractal Low of degree 13
indicator_fractal_high_degree21_column_name="fh21" # Fractal High of degree 21
indicator_fractal_low_degree21_column_name="fl21" # Fractal Low of degree 21
indicator_fractal_high_degree34_column_name="fh34" # Fractal High of degree 34
indicator_fractal_low_degree34_column_name="fl34" # Fractal Low of degree 34
indicator_fractal_high_degree55_column_name="fh55" # Fractal High of degree 55
indicator_fractal_low_degree55_column_name="fl55" # Fractal Low of degree 55
indicator_fractal_high_degree89_column_name="fh89" # Fractal High of degree 89
indicator_fractal_low_degree89_column_name="fl89" # Fractal Low of degree 89



# %%


#--@STCGoal PDS Utils

#@title Range shift add col drop na
def jgtpd_col_add_range_shifting_dropnas(dfsrc,ctxcolname='ao',colprefix='pao',endrange=10):
  return jgtpd_dropnas_on_any_rows(jgtpd_col_add_range_shifting(dfsrc,ctxcolname,colprefix,endrange))

#@title BACKWARD Range shift col
def jgtpd_col_add_range_shifting(dfsrc,ctxcolname='ao',colprefix='pao',endrange=10):
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
def pds_get_dt_from_and_to_for_now_live_price(_timeframe,_nbbar2retrieve=335,quiet=True):
  _nbmintf=getMinByTF(_timeframe)
  now=datetime.datetime.now(datetime.timezone.utc)
  weekdayoffset=0
  chkweekday=now.weekday()
  #chkweekday=0 #simulating
  if not quiet:
    print('Weekday is: ' + str(chkweekday))
  if chkweekday == 7:
    weekdayoffset=1440
  if chkweekday == 0:
    weekdayoffset=2840
  _idsIndiPrepNbBars=90
  dtminute = datetime.timedelta(minutes=_nbmintf*(_nbbar2retrieve+weekdayoffset+_idsIndiPrepNbBars))
  # --@STCIssue  when on the weekend
  #TODO CHECK MARKET CLOSE THEN STARTS FROM THERE
  datefromobj =now - dtminute
  datefrom = datefromobj.strftime(_dtformat)
  #ref format:.str('%m.%d.%Y %H:%M:%S')
  nowstring=now.strftime(_dtformat)
  dateto = nowstring
  # print('NOW String used: ' + nowstring)
  # print('Pov:'+ pov)
  # print('From:' + datefrom)
  # print('To:  ' + dateto)
  return datefrom,dateto


# %%
#--@STCGoal IDS Indicators and related / CDS



def ids_add_indicators(__df,
                       enableGatorOscillator=False,
                       enableMFI=False,
                       dropnavalue=True,
                       quiet=False,                       
                       cleanupOriginalColumn=True,useLEGACY=True):
  if not useLEGACY: # Because jgtapy has to be upgraded with new column name, we wont use it until our next release
    return Indicators.jgt_create_ids_indicators_as_dataframe(__df,
                       enableGatorOscillator,
                       enableMFI,                          
                       cleanupOriginalColumn,                    
                       quiet)
  else:
    return ids_add_indicators_LEGACY(__df,
                       enableGatorOscillator,
                       enableMFI,
                       dropnavalue,
                       quiet)

def ids_add_indicators_LEGACY(__df,
                       enableGatorOscillator=False,
                       enableMFI=False,
                       dropnavalue=True,
                       quiet=False):
  if not quiet:
    print("Adding indicators...")
  i=Indicators(__df)
  
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
    i.gator(period_jaws=13, period_teeth=8, period_lips=5, shift_jaws=8, shift_teeth=5, shift_lips=3, column_name_val1='gl', column_name_val2='gh')
  if enableMFI:
    i.bw_mfi(column_name='mfi')
  _df=i.df
  if dropnavalue:
    _df = _df.dropna()
  try: 
    _df=_df.set_index('Date')
  except TypeError:
    pass
  if not quiet:
    print("done adding indicators :)")
  return _df


# %%
#@title Pandas JGT Utilities
def jgtpd_dropnas_on_any_rows(_df):
	return _df.dropna(axis='rows')
	
def jgtpd_drop_cols_from_to_by_name(_df,firstcolname,lastcolname,_axis = 1):
  return _df.drop(_df.loc[:, firstcolname:lastcolname].columns,axis = _axis)


def jgtpd_col_drop_range(_df,colprefix='pao',endrange=10):
	_firstcolname=colprefix+str(1)
	_lastcolname=colprefix+str(endrange)
	return jgtpd_drop_cols_from_to_by_name(_df,_firstcolname,_lastcolname,1)



def ids_add_fdb_intermediaries_columns(_df):
    
  #Bullish
  _df['HighisBellowLips'] = _df.lips > _df.High

  _df['LowIsLower']= _df.Low < _df.Low.shift()

  _df['ClosedAboveMedian'] = _df.Close > _df.Median

  #Bearish

  _df['LowisAboveLips'] = _df.lips < _df.Low

  _df['HighIsHigher']= _df.High > _df.High.shift()

  _df['ClosedBellowMedian'] = _df.Close < _df.Median
  return _df


def ids_clear_fdb_intermediaries_columns(_df,quiet=False):
  try:
    _df =jgtpd_drop_cols_from_to_by_name(_df,
          'HighisBellowLips',
        'ClosedBellowMedian')
  except KeyError:
    print("Might cleared already")
    pass
  return _df

  # try:
  #   dfcln =jgtpd_drop_cols_from_to_by_name(dfcln,
  #         'HighisBellowLips',
  #       'ClosedAboveMedian')
  # except KeyError:
  #   print("Might cleared already")
  #   pass


#@title FDB Bullish logics
#from : https://stackoverflow.com/questions/23330654/update-a-dataframe-in-pandas-while-iterating-row-by-row

def ids_add_fdb_column_logics(_df,
                              _dropIntermediariesColumns=True,
                              quiet=False):
  _df=ids_add_fdb_intermediaries_columns(_df)
  for i, row in _df.iterrows():

      ClosedAboveMedian = _df.at[i,'ClosedAboveMedian']
      LowIsLower = _df.at[i,'LowIsLower']
      HighisBellowLips  = _df.at[i,'HighisBellowLips']
      ClosedBellowMedian = _df.at[i,'ClosedBellowMedian']
      HighIsHigher = _df.at[i,'HighIsHigher']
      LowisAboveLips  = _df.at[i,'LowisAboveLips']


      ##################################################
      #########   FDBB
      isFDB = False
      isFDBCode = 0
      high=0
      low=0
      if HighisBellowLips and LowIsLower and ClosedAboveMedian   :
          isFDB = True
          isFDBCode=1
          high  = _df.at[i,'High']
          low  = _df.at[i,'Low']
      _df.at[i,'fdbbhigh'] = high 
      _df.at[i,'fdbblow'] = low 
      _df.at[i,'fdbb'] = isFDB    
      _df.at[i,'fdb'] = isFDBCode   # So we have All
      ##################################################
      #########   FDBS
      isFDB = False    
      isFDBCode = 0
      high=0
      low=0
      if LowisAboveLips and HighIsHigher and ClosedBellowMedian   :
          isFDB = True
          isFDBCode = -1
          high  = _df.at[i,'High']
          low  = _df.at[i,'Low']
          
      _df.at[i,'fdbshigh'] = high 
      _df.at[i,'fdbslow'] = low 
      _df.at[i,'fdbs'] = isFDB
      _df.at[i,'fdb'] = isFDBCode 
  if _dropIntermediariesColumns:
    _df = ids_clear_fdb_intermediaries_columns(_df,quiet=quiet)
  return _df








#@title AOF function pto (AO Fractals)



#@title Range shift col
def jgtids_mk_ao_fractal_peak(dfsrc,
                              ctxcolname='ao',
                              poscolprefix='pao',
                              negcolprefix='nao',
                              endrange=10,
                              quiet=False):
  """ Make the AO Fractal Peak

    Args:
         _df (DataFrame source)
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
    cur=dfsrc.at[i,'ao']
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
    ao_fractalPeakOfMomentum_column_name = 'aof'
    dfsrc.at[i,ao_fractalPeakOfMomentum_column_name]=barAOF
    ao_fractalPeakValue_column_name = 'aofvalue'
    dfsrc.at[i,ao_fractalPeakValue_column_name]=cur #current AO Value
    dfsrc.at[i,'aofhighao']=outHighAO #current High Price
    dfsrc.at[i,'aoflowao']=outLowAO #current Low Price
    dfsrc.at[i,'aofhigh']=outHigh #current High Price
    dfsrc.at[i,'aoflow']=outLow #current Low Price
  l_df = len(dfsrc)
  if not quiet:
    print("Total Peak - Up:" + str(countUpPeak) + ", Dn: " + str(countDownPeak) + " on total: " + str(l_df))
  dfsrc=__ids_cleanse_ao_peak_secondary_columns(dfsrc,True)
  return dfsrc












#@title Add CDS signals

def cds_add_signals_to_indicators(dfires,_aopeak_range=28,quiet=False):
  dfires=ids_add_fdb_column_logics(dfires,quiet=quiet)
  dfires = jgtids_mk_ao_fractal_peak(dfires,
                                   'ao',
                                   'p',
                                   'n',
                                   _aopeak_range,
                                   quiet=quiet)
  return dfires


def tocds(dfsrc):
  dfires = ids_add_indicators(dfsrc,quiet=True)
  dfires = cds_add_signals_to_indicators(dfires,quiet=True)
  dfires = jgti_add_zlc_plus_other_AO_signal(dfires,quiet=True)
  dfires = pds_cleanse_original_columns(dfires,quiet=True)
  dfires = __ids_cleanse_ao_peak_secondary_columns(dfires,quiet=True)
  return dfires











#@title PD Columen Cleanup Functions

def jgtpd_drop_col_by_name(_df,colname,_axis = 1,quiet=False):
  """Drop Column in DF by Name

  Args:
        _df (DataFrame source)
        ctxcolname (column name from)
        _axis (  axis)
        quiet (quiet output)
        
  Returns:
    Clean DataFrame 
  """
  if colname in _df.columns:
    return _df.drop(_df.loc[:, colname:colname].columns,axis = _axis)
  else:
    if not quiet:
      print('Col:' + colname + ' was not there')
    return _df

def __ids_cleanse_ao_peak_secondary_columns(dfsrc,quiet=False):
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p0',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p1',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p2',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p3',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p4',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p5',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p6',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p7',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p8',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p9',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p10',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p11',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p12',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p13',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p14',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p15',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p16',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p17',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p18',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p19',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p20',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p21',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p22',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p23',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p24',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p25',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p26',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p27',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p28',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p29',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'p30',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n0',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n1',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n2',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n3',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n4',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n5',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n6',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n7',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n8',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n9',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n10',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n11',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n12',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n13',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n14',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n15',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n16',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n17',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n18',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n19',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n20',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n21',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n22',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n23',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n24',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n25',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n26',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n27',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n28',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n29',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'n30',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao0',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao1',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao2',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao3',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao4',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao5',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao6',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao7',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao8',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao9',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao10',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao11',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao12',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao13',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao14',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao15',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao16',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao17',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao18',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao19',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao20',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao21',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao22',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao23',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao24',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao25',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao26',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao27',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao28',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao29',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pao30',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao0',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao1',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao2',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao3',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao4',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao5',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao6',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao7',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao8',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao9',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao10',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao11',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao12',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao13',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao14',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao15',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao16',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao17',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao18',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao19',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao20',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao21',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao22',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao23',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao24',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao25',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao26',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao27',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao28',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao29',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nao30',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pac0',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pac',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pac1',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pac2',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pac3',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pac4',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pac5',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pac6',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pac7',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pac8',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'pac9',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nac',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nac0',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nac1',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nac2',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nac3',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nac4',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nac5',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nac6',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nac7',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nac8',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'nac9',1,quiet) 
  return dfsrc

def pds_cleanse_original_columns(dfsrc,quiet=True):
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'AskHigh',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'BidHigh',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'AskLow',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'BidLow',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'AskClose',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'BidClose',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'BidOpen',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'AskOpen',1,quiet)
  return dfsrc

def pds_cleanse_extra_columns(dfsrc,quiet=True):
  dfsrc=pds_cleanse_original_columns(dfsrc,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'LowisBellowJaw',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'HighisAboveJaw',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'LowisBellowTeeth',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'HighisAboveTeeth',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'HighisAboveLips',1,quiet)
  dfsrc=jgtpd_drop_col_by_name(dfsrc,'LowisBellowLips',1,quiet)
  dfsrc=__ids_cleanse_ao_peak_secondary_columns(dfsrc,quiet)
  if not quiet:
    print("Columns cleanup was executed")
  return dfsrc








# def Gethistoryprice(instrument,timeframe,number=300):
#   con.get_candles('EUR/USD', period='m1', number=100)


def fdb_print_info(df,isBuy=True):
  n='fdbs'
  c='low'
  if isBuy:
    n='fdbb'
    c='high'
  cn= n+c
  for i in df:
    h=df[i]['fdbshigh']
    print(h)
  
  
  
  
#@title ZLC Buy and Sell v2 2210161707 

def jgti_add_zlc_plus_other_AO_signal(_df,dropsecondaries=True,quiet=True):
  _df=jgtpd_col_add_range_shifting(_df,'ao','pao',10)
  _df=jgtpd_col_add_range_shifting(_df,'ac','pac',4)
  if not quiet:
    print('----added shofted range AO')
  _df['aoaz']= _df['ao']>0
  _df['aobz']= _df['ao']<0
  #_df['zlcb']=_df[_df['ao']]
  c=0
  xc=len(_df)
  for i,row in _df.iterrows():
    c=c+1
    cao=_df.at[i,'ao']
    cac=_df.at[i,'ac']
    pac1=_df.at[i,'pac1']
    pac2=_df.at[i,'pac2']
    pac3=_df.at[i,'pac3']
    cacgreen = False
    pac1green=False
    pac2green=False
    if cac > pac1:
      cacgreen=True
    if pac1 > pac2:
      pac1green=True
    if pac2 > pac3:
      pac2green=True
    
    pao1=_df.at[i,'pao1']
    pao2=_df.at[i,'pao2']
    pao3=_df.at[i,'pao3']
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
    
    
    aoaz=_df.at[i,'aoaz']
    aobz=_df.at[i,'aobz']

    #ZLC
    isZLCBuy = False
    isZLCSell = False
    zlcCode=0
    if pao1 > 0 and aobz == True:
      zlcCode = -1
      isZLCSell=True
    if pao1 < 0 and aoaz == True:
      zlcCode = 1
      isZLCBuy=True
    
    zeroLineCrossingSignalCode_column_name = 'zlc'
    _df.at[i,zeroLineCrossingSignalCode_column_name] = zlcCode  
    zeroLineCrossingBuySignal_column_name = 'zlcb'
    _df.at[i,zeroLineCrossingBuySignal_column_name] = isZLCBuy
    zeroLineCrossingSellSignal_column_name = 'zlcs'
    _df.at[i,zeroLineCrossingSellSignal_column_name] = isZLCSell

    #Coloring AO
    if caogreen:
      _df.at[i,'aocolor'] = 'rgb(0,255,0)'
    else:
      _df.at[i,'aocolor'] = 'rgb(255,0,0)'
      
    #Coloring AC
    if cacgreen:
      _df.at[i,'accolor'] = 'rgb(0,255,0)'
    else:
      _df.at[i,'accolor'] = 'rgb(255,0,0)'
      
    
    # --@STCIssue Zone  (Not sure, it might have to be ABove or Bellow)
    nonTradingZoneColor = 'gray'
    zoneColor = nonTradingZoneColor                #default Zone Color
    
    sellingZoneColor = 'red'
    buyingZoneColor = 'green'
    
    redZone = False
    if cacred and caored and pac1red and pao1red:
      redZone=True
      zoneColor = sellingZoneColor

    greenZone = False
    if cacgreen and caogreen and pac1green and pao1green:
      greenZone=True
      zoneColor=buyingZoneColor
      
    _df.at[i,'zcol'] = zoneColor
    
    #Sell Zone Signal
    sellZoneSignal_column_name = 'sz'
    _df.at[i,sellZoneSignal_column_name]=redZone
    
    #Buy Zone Signal
    buyZoneSinal_column_name = 'bz'
    _df.at[i,buyZoneSinal_column_name]=greenZone
    
    #AC Sell / Buy  3 AC Against AO af AC Bellow, 2 if above
    acSell = False
    msgacSignal = "No "
    if cacred and pac1red and caogreen and pao1green:
      acSell=True      
      if cac < 0 and pac2green:# We require 3 bars red on the AC When bellow zero
        acSell=False
    acBuy = False
    if cacgreen and pac1green and caored and pao1red:
      acBuy=True
      if cac>0 and pac2red:        
        acBuy=False
    
    #AC Sell Signal (Deceleration)
    deceleration_ACSignal_column_name = 'acs'
    _df.at[i,deceleration_ACSignal_column_name]=acSell
    
    #AC Buy Signal (Acceleration)
    acceleration_ACSignal_column_name = 'acb'
    _df.at[i,acceleration_ACSignal_column_name]=acBuy
    
    if acSell and not quiet:
      print("AC Sell Signal with AC Bellow Zero Line "+ str(i))
    if acBuy and not quiet:
      print("AC Buy Signal with AC ABove Zero Line "+ str(i))
    
    #Saucer Strategy
    # More on Saucer Strategy : http://simp.ly/p/2K1HBr
    saucerSell=False
    if cao < 0 and caored and pao1green and pao2green :
      saucerSell=True
      
    saucerBuy=False
    if cao > 0 and caogreen and pao1red and pao2red:
      saucerBuy=True
    saucerSellSignal_column_name = 'ss'
    _df.at[i,saucerSellSignal_column_name]=saucerSell
    saucerBuySignal_column_name = 'sb'
    _df.at[i,saucerBuySignal_column_name]=saucerBuy
    
    # What Happens on the Next PLUS 35 Periods ??
    if c < xc - 35:
      cPrice = row['Close']
    # What Happens on the Next PLUS 55 Periods ??
  return _df
    