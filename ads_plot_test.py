import pandas as pd; import numpy as np;import jgtpy.JGTPDSP as pds;import jgtpy.JGTIDS as ids;import jgtpy.JGTCDS as cds;instrument='EUR/USD';timeframe='H4';print('variable instrument,timeframe are defined.  imported  pdsp,ids,cds,ads,ah');import jgtpy;i=instrument;t=timeframe;df=pd.read_csv('./data/pds/EUR-USD_H4.csv');c=ids.tocds(df);import jgtpy.JGTADS as ads;import jgtpy.adshelper as a
ads.plot_from_cds_df(c,i,t,plot_ao_peaks=True)

