# %% imports
from matplotlib import pyplot as plt
import jgtpy as jgt

# jgt.help()

# %% test

i = "SPX500"
t = "H1"
rq = jgt.ads_request(
    instrument=i,
    timeframe=t,
    show=True,
    peak_distance=21,
    peak_width=13,
    plot_ao_peaks=True,
)



# %% ADS       PERSPECTIVE
# use_fresh = True rq.crop_last_dt = None
rq.crop_last_dt = None
rq.timeframe = "H4"
rq.__timeframes__("M1,W1,D1,H4,H1")
rq.use_fresh = False
#print(rq)
#%%
p = jgt.plot_perspective(rq)

# %% p
p

# %%
rq.timeframes


#%%
p["H4"]["fig"]

#%%

myperspective=p["H4"]
myperspective["fig"]

# %%
for tf in rq.timeframes:
    #print(tf)
    _p={}
    _p=p[tf]
    chart=_p["fig"]
    chart

















# %% rq copy
rq2 = rq.copy_with_timeframe("H8")
# rq2.timeframe = "H8"
rq2.__dict__


# %% ADS
fig, arr, _ads_df = jgt.ads_create_v2(rq, True)


# %% ADS
# use_fresh = True rq.crop_last_dt = None
rq.crop_last_dt = None
rq.use_fresh = True
fig, arr, _ads_df = jgt.ads_create_v2(rq, True)


# %% ADS
#  CROP
rq.crop_last_dt = "2024-02-28 12:00"
# rq.use_fresh = True
rq.quiet = False
fig, arr, _ads_df = jgt.ads_create_v2(rq, True)


# %% ADS
#  CROP
rq.crop_last_dt = "2024-03-05 12:00"
# rq.use_fresh = True
fig, arr, _ads_df = jgt.ads_create_v2(rq, True)


# %% ADS        = "H4"
# use_fresh = True rq.crop_last_dt = None
rq.crop_last_dt = None
rq.timeframe = "H4"
rq.use_fresh = True
fig, arr, _ads_df = jgt.ads_create_v2(rq, True)


# %%
_ads_df


# %%
fig.__dict__

# %%
arr

# %%
_ads_df.__dict__

# %% Proto plotly having the arr and fig
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
import numpy as np

# make plot using returned arr and fig above


# %% ADS  with fresh data
ads_fresh_chart, _ads_fresh_plt_arr, _ads_fresh_df = jgt.ads_create(
    i, t, use_fresh=True
)
ads_fresh_chart.show()


# %%
crop_dt = "2023-01-13 21:00"
ads_crop_chart, _ads_crop_plt_arr, _ads_crop_df = jgt.ads_create(
    i, t, crop_last_dt=crop_dt
)
ads_crop_chart.show()


# %% Try to plot tf m15 that is not up to date with now
t = "m15"
ads_m15_chart, _ads_m15_plt_arr, _ads_m15_df = jgt.ads_create(i, t)

# %% Select a crop date that we dont have data yet for it
crop_dt = "2024-02-29 21:00"
ads_m15_chart2, _ads_m15_plt_arr2, _ads_m15_df2 = jgt.ads_create(
    i, t, crop_last_dt=crop_dt
)


# %%
df = jgt.read(i, t)
df.tail(1)


# %% CDS
df = jgt.cds_create(i, t)

df.tail(1)
# %%
df_fresh = jgt.cds_create(i, t, use_fresh=True)
df_fresh.tail(1)

# %%
df_fresh_full = jgt.cds_create(i, t, use_fresh=True, use_full=True)
df_fresh_full.head(1)
# %%
len(df_fresh_full)

# MKS
jgt.mksg_by_crop_dates(
    i,
    t,
    "H4",
    "Fractal",
    "2023-01-01",
    scn_root_dir="./build",
    show_chart=False,
    show_tabs=True,
    save_fig_image=True,
    save_cds_data=True,
)


# %%
fig.__dict__

# %% Serialize import pickle
import pickle

# Save the Matplotlib figure using pickle
with open("figure_data.pickle", "wb") as file:
    pickle.dump(fig, file)

# %% Load it back
# Load the Matplotlib figure from the pickle file
with open("figure_data.pickle", "rb") as file:
    loaded_figure = pickle.load(file)

loaded_figure.__dict__

# %%
loaded_figure
# Display the loaded figure
# plt.figure(loaded_figure.number)
# plt.figure
