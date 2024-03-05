# %% Imports
from jgtpy import JGTCDS as cds,JGTIDS as ids,JGTPDSP as pds
from jgtpy.JGTCDSRequest import JGTCDSRequest


# %%
i="EUR/USD"
i="SPX500"
t="H4"  # REMOVED it so it should be got by wslhelper

#%% Test IDS first
df=pds.getPH(i,t)

#%%
df.tail(1)

#%% 

# %%
rq=JGTCDSRequest()
rq.peak_distance=13
rq.peak_width=8
rq.peak_divider_min_height=2

#%% #@q Can we call tocds with JGTCDSRequest?YES
dfcds = ids.tocds(df, rq=rq)

#%%
dfcds.tail(1)

# %%
rq.__dict__
# %%
r=cds.create(i, t, rq=rq)
# %%
r.tail(1)
# %%
r.head(1)

# %%
