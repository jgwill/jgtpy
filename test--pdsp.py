# %% Imports PDSP
import jgtpy.JGTPDSP as pds

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
print(os.getenv("JGTPY_DATA"))
JGTPY_DATA=os.getenv("JGTPY_DATA")


#%% INstruments + tf

# Instrument def
instrument = "EUR/USD"
instrument = "XAU/USD"
instrument = "SPX500"
instrument = "WHEATF"
t="M1"

#%% Read manually the file using Pandas
ifn = instrument.replace("/","-")
csv_fn = os.path.join(JGTPY_DATA,"pds",ifn +"_"+t+".csv")
csv_fn
#%% Read manually the file using Pandas
mdf = pd.read_csv(csv_fn)
mdf

# %%
df=pds.getPH(instrument,t)
# %%
df
# %%
