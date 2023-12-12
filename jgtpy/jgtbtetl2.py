#from __init__ import env,jsonfile2prop,d2p,createByRange

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTCore import env,jsonfile2prop,d2p
from JGTCDS import  createByRange

import pandas as pd
from functools import reduce

# from jgtpy import env 
ctx=d2p(env)

trainsetfnjson=env['trainfnjson'] 
trainsetfncsv=env['trainfncsv'] 

dst=jsonfile2prop(trainsetfnjson)
l=0
for key, value in dst.items():
  l=key
lastitem=d2p(dst[l])
# print(lastitem)
# print(lastitem.state)
# print(lastitem.plx)
# print(lastitem.bs)
print('export lastdt="' + lastitem.dt+ '"')
# ctx['lastdt']=lastitem.dt
# df=createByRange(ctx.instrument,ctx.timeframe,ctx.firstst,lastitem.dt)
fnids=ctx.tsfnbase+".ids.csv"
# df.to_csv(fnids)

# #

fnbase=ctx.tsfnbase
# fn=fnbase + ".trainset.csv"
fn=trainsetfncsv
fnfix=fn.replace('.csv','f.csv')
fnfdbb=fnbase + ".fdb."+ctx.bs+".csv"
fnplx=fnbase + ".plx.csv"
fnplxtt=fnbase + ".plxtwintrade.csv"
fnloss=fnbase + ".loss.csv"
fnwin=fnbase + ".win.csv"
fnrrstotc=fnbase + ".rrstotc.csv"
fnidstrainmerged=fnbase + ".idstrainmerged.csv"
fnidstrainmergedouter=fnbase + ".idstrainmergedouter.csv"
from datetime import datetime
from datetime import timedelta
def offsetdt(time_str,nbhoursoffset=4,date_format_str= '%m/%d/%Y %H:%M:%S',output_dt_format='%Y-%m-%d %H:%M:%S'):
  given_time = datetime.strptime(time_str, date_format_str)
  final_time = given_time + timedelta(hours=nbhoursoffset)
  final_time_str = final_time.strftime(output_dt_format) 
  return final_time_str
  
def fixdtindf(_df,fieldname="dt",n=4):
  date_format_str = '%m/%d/%Y %H:%M:%S' #06/08/2022 09:00:00
  dfo=pd.DataFrame()
  for index,row in _df.iterrows():
    #print(index)
    # Given timestamp in string
    time_str = row[fieldname]
    # create datetime object from timestamp string
    given_time = datetime.strptime(time_str, date_format_str)
    #print('Given Time: ', given_time)
    # Add 2 hours to datetime object
    final_time = given_time + timedelta(hours=n)
    #print('Final Time : ', final_time)
    # Convert datetime object to string in specific format 
    final_time_str = final_time.strftime('%Y-%m-%d %H:%M:%S') #2022-06-08 13:00:00
    #print('Final Time as string object: ', final_time_str)
    _df.at[index,fieldname]=final_time_str
    #_df[index][fieldname]=final_time_str
    # row['dt'] = final_time_str
    #df[index]['dt'] = final_time_str
    #dfo[index]=row
  return _df
  
#df=pd.DataFrame()
df=pd.read_csv(fn) #TRainSET
# df=pd.read_csv(fn, header=0, parse_dates=["dt","plxdt"]) #TRainSET
df.index.rename('no',inplace=True)
#print(df)
df=fixdtindf(df,'dt')
df=fixdtindf(df,'plxdt')
#print(df)
df.to_csv(fnfix)
fdbdf=pd.DataFrame()
fdbTag='FDBB'
if ctx.bs=='Sell':
  fdbTag='FDBS'
fdbdf=df[df['sig']== fdbTag]
dfloss=df[df['state']== 'loss']
dfwin=df[df['state']== 'profit']
dfwin.to_csv(fnwin)
dfloss.to_csv(fnloss)
fdbdf.to_csv(fnfdbb)
dfplx=fdbdf[['bp','state','plx','plxc','tpl','tplc','to','tc','bs','dt','plxdt','i','tdt','oid','tid','r','ro','rs','rsx','sig','tf','tm']]
totplx=dfplx['plx'].sum()
tottpl=dfplx['tpl'].sum()
print(totplx)
print(tottpl)
dfrrstotc=fdbdf[['bp','state','plx','tpl','r','to','rs','tc','ro','plxc','tplc','bs','dt','plxdt','i','tdt','oid','tid','rsx','sig','tf','tm']]
dfplxtt=dfrrstotc[dfrrstotc['plx'] > (dfrrstotc['tplc'] * -1)]
dfplxtt.to_csv(fnplxtt)
#fdbdf.index.rename('bp',inplace=True)
dfplx.to_csv(fnplx)
dfrrstotc.to_csv(fnrrstotc)



# Merge
idsdf=pd.read_csv(fnids, index_col=["Date"],        parse_dates=["Date"])
fdbdfDIM = pd.read_csv(fnfdbb,
        header=0,
        index_col=["dt"],
        parse_dates=["dt","plxdt"])
        # names=["bp","bs","dt","plx","plxc","plxdt","r","ro","rs","sig","state","tc","tf","to","tpl","tplc"],
        # usecols=["bp","bs","dt","plx","plxc","plxdt","r","ro","rs","sig","state","tc","tf","to","tpl","tplc"],

# fdbdf.index.rename('Date',inplace=True)
fdbdfDIM.index.rename('Date',inplace=True)
data_frames = [idsdf,fdbdfDIM]

# df_merged_outer = reduce(lambda  left,right: pd.merge(left,right,                                            how='outer'), data_frames).fillna('void')
# df_merged_outer = reduce(lambda  left,right: pd.merge(left,right,on=['Date'],                                            how='outer'), data_frames)
df_mergedDIM = reduce(lambda  left,right: pd.merge(left,right,on=['Date'],  how='right'), data_frames).fillna('void')
df_mergedDIM.to_csv(fnidstrainmerged)
# df_merged_outer.to_csv(fnidstrainmergedouter)


