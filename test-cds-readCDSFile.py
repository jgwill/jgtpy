# %% Import cds
from jgtpy import JGTCDS as cds

# %% test read cds from file
read_full=True
cdf = cds.readCDSFile("SPX500", "H4", read_full=read_full)

# %%
cdf
# %%
