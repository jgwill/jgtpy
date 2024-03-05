# %% imports
from matplotlib import pyplot as plt
import jgtpy as jgt

jgt.help()

# %% test

i = "SPX500"
t = "H4"


# %% ADS
ads_chart, _ads_plt_arr, _ads_df = jgt.ads(i, t)
ads_chart.show()


# %% ADS  with fresh data
ads_fresh_chart, _ads_fresh_plt_arr, _ads_fresh_df = jgt.ads(i, t, use_fresh=True)
ads_fresh_chart.show()


# %%
crop_dt = "2023-01-13 21:00"
ads_crop_chart, _ads_crop_plt_arr, _ads_crop_df = jgt.ads(i, t, crop_last_dt=crop_dt)
ads_crop_chart.show()


#%% Try to plot tf m15 that is not up to date with now
t="m15"
ads_m15_chart, _ads_m15_plt_arr, _ads_m15_df = jgt.ads(i, t)

#%% Select a crop date that we dont have data yet for it
crop_dt = "2024-02-29 21:00"
ads_m15_chart2, _ads_m15_plt_arr2, _ads_m15_df2 = jgt.ads(i, t, crop_last_dt=crop_dt)


# %%
df = jgt.read(i, t)
df.tail(1)


# %% CDS
df = jgt.cds(i, t)

df.tail(1)
# %%
df_fresh = jgt.cds(i, t, use_fresh=True)
df_fresh.tail(1)

# %%
df_fresh_full = jgt.cds(i, t, use_fresh=True, use_full=True)
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







#%% 
ads_chart.__dict__

# %% Serialize import pickle
import pickle
# Save the Matplotlib figure using pickle
with open('figure_data.pickle', 'wb') as file:
    pickle.dump(ads_chart, file)

#%% Load it back
# Load the Matplotlib figure from the pickle file
with open('figure_data.pickle', 'rb') as file:
    loaded_figure = pickle.load(file)

loaded_figure.__dict__

#%%
loaded_figure
# Display the loaded figure
#plt.figure(loaded_figure.number)
#plt.figure