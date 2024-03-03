# %% Imports JGTIDS
import jgtpy.JGTIDS as ids
import jgtpy.JGTPDSP as pds


#%% 
# Instrument
i="CORNF" #@STCIssue M1 (74f), W1 (less than 313 frames)
i="EUR/USD"
i="WHEATF"
i="SPX500"
t="M1"
t="W1"
t="D1"

#%%
p=pds.getPH(i,t)
len(p)

#%%
i2=ids.ids_add_indicators(p,bypass_index_reset=False,quiet=True,big_alligator=True)

#%%
i=ids.tocds(p)

#%%
i.to_csv("test-ids-240107.csv")
# %%
