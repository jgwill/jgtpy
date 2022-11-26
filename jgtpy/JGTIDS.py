# %%
#@title FDB Intermediary values
#@title Add Indicators Columns
import pandas as pd
import datetime
_dtformat = '%m.%d.%Y %H:%M:%S'
# %%


#--@STCGoal PDS Utils

#@title Range shift add col drop na
def jgtpd_col_add_range_shifting_dropnas(_df,ctxcolname='ao',colprefix='pao',endrange=10):
  return jgtpd_dropnas_on_any_rows(jgtpd_col_add_range_shifting(_df,ctxcolname,colprefix,endrange))

#@title BACKWARD Range shift col
def jgtpd_col_add_range_shifting(_df,ctxcolname='ao',colprefix='pao',endrange=10):
  """Add a BACKWARD range of shifted values
    for a column with a prefixed numbered.

    Args:
         _df (DataFrame source)
         ctxcolname (column name from)
         colprefix (new columns prefix)
         endrange (the end of the range from 0)
         
    Returns:
      DataFrame with new columns
  """
  for i in range(endrange):
    _df[colprefix+str(i)]=_df[ctxcolname].shift(i)
  return _df

  
  
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

from jgtapy import Indicators
def ids_add_indicators(__df,
                       enableGatorOscillator=False,
                       enableMFI=False,
                       dropnavalue=True,
                       quiet=False,                       
                       cleanupOriginalColumn=True):
  return Indicators.jgt_create_ids_indicators_as_dataframe(__df,
                       enableGatorOscillator,
                       enableMFI,                          
                       cleanupOriginalColumn,                    
                       quiet)

def ids_add_indicators_LEGACY(__df,
                       enableGatorOscillator=False,
                       enableMFI=False,
                       dropnavalue=True,
                       quiet=False):
  if not quiet:
    print("Adding indicators...")
  i=Indicators(__df)
  i.accelerator_oscillator( column_name= 'ac')
  i.alligator(period_jaws=13, period_teeth=8, period_lips=5, shift_jaws=8, shift_teeth=5, shift_lips=3, column_name_jaws='jaw', column_name_teeth='teeth', column_name_lips='lips')
  i.alligator(period_jaws=89, period_teeth=55, period_lips=34, shift_jaws=55, shift_teeth=34, shift_lips=21, column_name_jaws='bjaw', column_name_teeth='bteeth', column_name_lips='blips')
  i.awesome_oscillator(column_name='ao')
  i.fractals(column_name_high='fb', column_name_low='fs')
  i.fractals3(column_name_high='fb3', column_name_low='fs3')
  i.fractals5(column_name_high='fb5', column_name_low='fs5')
  i.fractals8(column_name_high='fb8', column_name_low='fs8')
  i.fractals13(column_name_high='fb13', column_name_low='fs13')
  i.fractals21(column_name_high='fb21', column_name_low='fs21')
  i.fractals34(column_name_high='fb34', column_name_low='fs34')
  i.fractals55(column_name_high='fb55', column_name_low='fs55')
  i.fractals89(column_name_high='fb89', column_name_low='fs89')
  
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
def jgtids_mk_ao_fractal_peak(_df,
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
  _l=len(_df)
  for o in range(endrange):   
    i=int(o-half)
    #if o < (_l - half) and (o > half):
    _cn=poscolprefix+str(i)
    if i < 0:
      _cn=negcolprefix+str(i).replace('-','')
    _df[_cn]=_df[ctxcolname].shift(i)
    #print(_cn + '= _df.at[i,\''+_cn+'\']')
    #print('_df = jgtpd_drop_col_by_name(_df,\''+_cn+'\')')
    #else:
    #  print("We are not in range yet :" + str(i))

  _std = _df[ctxcolname].std()
  _max = _df[ctxcolname].max()
  _min = _df[ctxcolname].min()
  _filterOutAOFThreshold_ABOVE = (_std + _max) / 2
  _filterOutAOFThreshold_BELLOW = ((_std * -1) + _min) / 2
  
  if not quiet:
    print("filterout (std) Above(max)/(min)Bellow:  ("+ str(_std) + ")  " + str(_filterOutAOFThreshold_ABOVE) + "(" + str(_max) + ") / (" + str(_min) + ") " + str(_filterOutAOFThreshold_BELLOW))
  
  #
  countUpPeak=0
  countDownPeak=0
  countDiscarted=0
  for i,row in _df.iterrows():
    barAOF = 0
    dt=i
    curHigh= _df.at[i,'High']
    curLow= _df.at[i,'Low']
    cur=_df.at[i,'ao']
    n9= _df.at[i,'n9']
    n13= _df.at[i,'n13']
    n12= _df.at[i,'n12']
    n11= _df.at[i,'n11']
    n10= _df.at[i,'n10']
    n8= _df.at[i,'n8']
    n7= _df.at[i,'n7']
    n6= _df.at[i,'n6']
    n5= _df.at[i,'n5']
    n4= _df.at[i,'n4']
    n3= _df.at[i,'n3']
    n2= _df.at[i,'n2']
    n1= _df.at[i,'n1']
    p0= _df.at[i,'p0']
    p1= _df.at[i,'p1']
    p2= _df.at[i,'p2']
    p3= _df.at[i,'p3']
    p4= _df.at[i,'p4']
    p5= _df.at[i,'p5']
    p6= _df.at[i,'p6']
    p7= _df.at[i,'p7']
    p8= _df.at[i,'p8']
    p9= _df.at[i,'p9']
    p10= _df.at[i,'p10']
    p11= _df.at[i,'p11']
    p12= _df.at[i,'p12']
    p13= _df.at[i,'p13']

    outHigh=0
    outHighAO=0
    outLow=0
    outLowAO=0
    #print(str(i)+'::cur > p1 {'+ str(cur) + ' > ' + str(p1))
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
      if cur > 0 and cur > _filterOutAOFThreshold_ABOVE:
        barAOF=21        
        if not quiet:
          print("We have an up peak at:" + str(dt))
        countUpPeak=countUpPeak+1
      else:
        if cur >0 and cur > _std and barAOF != 21:
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
        if cur < 0 and cur < _filterOutAOFThreshold_BELLOW:
          barAOF=-21          
          if not quiet:
            print("We have an down peak at: " + str(dt))
          countDownPeak=countDownPeak+1
        else :
          if cur < 0 and cur < _std*-1 and barAOF != -21:
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
    _df.at[i,'aof']=barAOF
    _df.at[i,'aofvalue']=cur #current AO Value
    _df.at[i,'aofhighao']=outHighAO #current High Price
    _df.at[i,'aoflowao']=outLowAO #current Low Price
    _df.at[i,'aofhigh']=outHigh #current High Price
    _df.at[i,'aoflow']=outLow #current Low Price
  _l = len(_df)
  if not quiet:
    print("Total Peak - Up:" + str(countUpPeak) + ", Dn: " + str(countDownPeak) + " on total: " + str(_l))
  _df=__ids_cleanse_ao_peak_secondary_columns(_df,True)
  return _df












#@title Add CDS signals

def cds_add_signals_to_indicators(_dfi,_aopeak_range=28,quiet=False):
  _dfi=ids_add_fdb_column_logics(_dfi,quiet=quiet)
  _dfi = jgtids_mk_ao_fractal_peak(_dfi,
                                   'ao',
                                   'p',
                                   'n',
                                   _aopeak_range,
                                   quiet=quiet)
  return _dfi

def tocds(_df):
  _dfi = ids_add_indicators(_df,quiet=True)
  _dfi = cds_add_signals_to_indicators(_dfi,quiet=True)
  _dfi = jgti_add_zlc_plus_other_AO_signal(_dfi,quiet=True)
  _dfi = pds_cleanse_original_columns(_dfi,quiet=True)
  _dfi = __ids_cleanse_ao_peak_secondary_columns(_dfi,quiet=True)
  return _dfi











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

def __ids_cleanse_ao_peak_secondary_columns(_df,quiet=False):
  _df=jgtpd_drop_col_by_name(_df,'p0',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p1',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p2',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p3',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p4',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p5',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p6',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p7',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p8',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p9',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p10',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p11',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p12',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p13',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p14',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p15',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p16',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p17',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p18',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p19',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p20',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p21',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p22',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p23',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p24',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p25',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p26',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p27',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p28',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p29',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'p30',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n0',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n1',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n2',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n3',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n4',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n5',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n6',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n7',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n8',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n9',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n10',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n11',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n12',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n13',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n14',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n15',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n16',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n17',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n18',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n19',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n20',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n21',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n22',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n23',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n24',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n25',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n26',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n27',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n28',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n29',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'n30',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao0',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao1',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao2',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao3',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao4',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao5',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao6',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao7',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao8',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao9',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao10',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao11',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao12',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao13',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao14',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao15',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao16',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao17',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao18',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao19',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao20',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao21',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao22',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao23',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao24',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao25',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao26',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao27',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao28',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao29',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pao30',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao0',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao1',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao2',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao3',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao4',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao5',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao6',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao7',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao8',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao9',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao10',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao11',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao12',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao13',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao14',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao15',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao16',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao17',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao18',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao19',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao20',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao21',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao22',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao23',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao24',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao25',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao26',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao27',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao28',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao29',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nao30',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac0',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac1',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac2',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac3',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac4',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac5',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac6',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac7',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac8',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'pac9',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac0',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac1',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac2',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac3',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac4',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac5',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac6',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac7',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac8',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'nac9',1,quiet) 
  return _df

def pds_cleanse_original_columns(_df,quiet=True):
  _df=jgtpd_drop_col_by_name(_df,'AskHigh',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'BidHigh',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'AskLow',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'BidLow',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'AskClose',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'BidClose',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'BidOpen',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'AskOpen',1,quiet)
  return _df

def pds_cleanse_extra_columns(_df,quiet=True):
  _df=pds_cleanse_original_columns(_df,quiet)
  _df=jgtpd_drop_col_by_name(_df,'LowisBellowJaw',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'HighisAboveJaw',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'LowisBellowTeeth',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'HighisAboveTeeth',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'HighisAboveLips',1,quiet)
  _df=jgtpd_drop_col_by_name(_df,'LowisBellowLips',1,quiet)
  _df=__ids_cleanse_ao_peak_secondary_columns(_df,quiet)
  if not quiet:
    print("Columns cleanup was executed")
  return _df








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
    _df.at[i,'zlc'] = zlcCode  
    _df.at[i,'zlcb'] = isZLCBuy
    _df.at[i,'zlcs'] = isZLCSell

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
    zoneColor = 'gray'                #default Zone Color
    
    redZone = False
    if cacred and caored and pac1red and pao1red:
      redZone=True
      zoneColor = 'red'

    greenZone = False
    if cacgreen and caogreen and pac1green and pao1green:
      greenZone=True
      zoneColor='green'
      
    _df.at[i,'zcol'] = zoneColor
    
    _df.at[i,'sz']=redZone
    _df.at[i,'bz']=greenZone
    
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
    _df.at[i,'acs']=acSell
    _df.at[i,'acb']=acBuy
    if acSell and not quiet:
      print("AC Sell Signal with AC Bellow Zero Line "+ str(i))
    if acBuy and not quiet:
      print("AC Buy Signal with AC ABove Zero Line "+ str(i))
    #Saucer
    saucerSell=False
    if cao < 0 and caored and pao1green and pao2green :
      saucerSell=True
      
    saucerBuy=False
    if cao > 0 and caogreen and pao1red and pao2red:
      saucerBuy=True
    _df.at[i,'ss']=saucerSell
    _df.at[i,'sb']=saucerBuy
    
    # What Happens on the Next PLUS 35 Periods ??
    if c < xc - 35:
      cPrice = row['Close']
    # What Happens on the Next PLUS 55 Periods ??
  return _df
    