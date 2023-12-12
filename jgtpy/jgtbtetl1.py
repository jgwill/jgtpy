
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTCore import env,jsonfile2prop,d2p
from JGTCDS import createByRange
import pandas as pd
from functools import reduce
import jgtetl
# from jgtpy import env 
ctx=d2p(env)

trainsetfnjson=env['trainfnjson'] 
trainsetfncsv=env['trainfncsv'] 

dtlast = ""
if hasattr(ctx, 'dtlast'):
  dtlast=ctx.dtlast
  print(dtlast)
else:
  dst=jsonfile2prop(trainsetfnjson)
  l=0
  for key, value in dst.items():
    l=key
  lastitem=d2p(dst[l])
  # print(lastitem)
  # print(lastitem.state)
  # print(lastitem.plx)
  # print(lastitem.bs)
  dtlast= lastitem.dt
  print('export lastdt="' + lastitem.dt+ '"')

print("The variable, dtlast is of type:", type(dtlast))
print("The variable, ctx.firstst is of type:", type(ctx.firstst))
dtfirst=ctx.firstst
dtfirst_with_offset=jgtetl.svc_offset_dt_by_tf(dtfirst,ctx.timeframe)

# jgtetl.offsetdt
#pto_nbhourbytfofoffset2212
# ctx['lastdt']=lastitem.dt
print("CReating CDS with Range: " + dtfirst_with_offset + " > " + dtlast)
df=createByRange(ctx.instrument,ctx.timeframe,dtfirst_with_offset,dtlast)
fnids=ctx.tsfnbase+".ids.csv"
df.to_csv(fnids)

#  SEE PART 02

# fnbase=ctx.tsfnbase
# # fn=fnbase + ".trainset.csv"
# fn=trainsetfncsv

# fnfdbb=fnbase + ".fdb."+ctx.bs+".csv"
# fnplx=fnbase + ".plx.csv"
# fnrrstotc=fnbase + ".rrstotc.csv"
# #df=pd.DataFrame()
# df=pd.read_csv(fn)
# df.index.rename('no',inplace=True)
# dfsel=pd.DataFrame()
# fdbTag='FDBB'
# if ctx.bs=='Sell':
#   fdbTag='FDBS'
# dfsel=df[df['sig']== fdbTag]
# dfsel.to_csv(fnfdbb)
# dfplx=dfsel[['bp','state','plx','plxc','tpl','tplc','to','tc','bs','dt','plxdt','i','tdt','oid','tid','r','ro','rs','rsx','sig','tf','tm']]
# totplx=dfplx['plx'].sum()
# print(totplx)
# dfrrstotc=dfsel[['bp','state','plx','tpl','r','to','rs','tc','ro','plxc','tplc','bs','dt','plxdt','i','tdt','oid','tid','rsx','sig','tf','tm']]
# #dfsel.index.rename('bp',inplace=True)
# dfplx.to_csv(fnplx)
# dfrrstotc.to_csv(fnrrstotc)
