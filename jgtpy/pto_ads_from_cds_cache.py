#%%
import os

i="SPX500"
ifn=i.replace("/","-")
t="m15"
base_dir=".."
spath=f"{base_dir}/tests/cds_data/{ifn}_{t}_cds_cache.csv"
if not os.path.exists(spath):
  base_dir="."
  spath=f"{base_dir}/tests/cds_data/{ifn}_{t}_cds_cache.csv"

import pandas as pd


df=pd.read_csv(spath,parse_dates=True,index_col=0)
# %%
import JGTADS as ads
import JGTADSRequest

# %%
save_additional_figures_path=f"{base_dir}/charts/{ifn}/{t}.png"
rq = JGTADSRequest.JGTADSRequest(instrument=i,timeframe=t,save_additional_figures_path=save_additional_figures_path)


# %%
fig,_,_=ads.plot_from_cds_df(df, rq=rq,show=False)
# %%
