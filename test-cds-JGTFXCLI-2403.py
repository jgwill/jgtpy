# %% Imports
from jgtpy import JGTCDS as cds, JGTIDS as ids, JGTPDSP as pds
from jgtpy.JGTCDSRequest import JGTCDSRequest

import os
# %%
i = "EUR/USD"
i = "SPX500"
t = "H4"  # REMOVED it so it should be got by wslhelper


#%% Test PDSP first
df=pds.getPH(i,t)

#%% #@q Did we got a new prices ?YES
df.tail(1)

#%% TRY to read FULL that dont exist
full=pds.getPH(i,t,use_full=True,run_jgtfxcli_on_error=True)

#%% Check full
full.head(1)


#%% Test PDSP FRESH
df=pds.getPH(i,t,use_fresh=True)

#%% #@q Did we got a new prices ?YES
df.tail(1)

#%% TRY to read FULL that dont exist
full=pds.getPH(i,t,use_full=True,run_jgtfxcli_on_error=True,use_fresh=True)

#%% Check full
full.head(1)
# %%
full.tail(1)









# %%
rq = JGTCDSRequest()
rq.peak_distance = 13
rq.peak_width = 8
rq.peak_divider_min_height = 2

# %%
rq.__dict__
# %%
print(i,t)
r = cds.create(i, t, rq=rq)
# %%
r.tail(1)
# %%
os.getenv("JGTPY_DATA")
# %%
