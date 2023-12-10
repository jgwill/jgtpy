# %% Import packages
from jgtpy import JGTADS as ads
from jgtpy import JGTPDSP as pds

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

instrument = "GBP/USD"
# %% Load data and plot all in one operation
show_plot=True
m1p=pds.getPH(instrument, "M1")

#%% Plot all charts in one operation

M1c, M1a = ads.plot_from_pds_df(m1p,instrument, "M1", show_plot=show_plot)
#M1c, M1a = ads.plot(instrument, "M1", show_plot=show_plot)

w1, w1a = ads.plot(instrument, "W1", show_plot=show_plot)
d1, d1a = ads.plot(instrument, "D1", show_plot=show_plot)

h4, h4a = ads.plot(instrument, "H4", show_plot=show_plot)
h1, h1a = ads.plot(instrument, "H1", show_plot=show_plot)
m15, m15a = ads.plot(instrument, "m15", show_plot=show_plot)
m5, m15a = ads.plot(instrument, "m5", show_plot=show_plot)
#mi1,mi1a = ads.plot(instrument, "m1", show_plot=show_plot)

# # %% Plot w1, d1,h4, h1 in four subplots
# print("--------------------------")
# print("Plot w1, d1,h4, h1 in four subplots")

# # Create the grid layout
# fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))

# axs[0, 0].imshow(w1)
# axs[0, 1].imshow(d1)
# axs[1, 1].imshow(h4)
# axs[1, 0].imshow(h1)

# # Customize the layout, labels, and titles if needed
# axs[0, 0].set_title("Chart 1")
# axs[0, 1].set_title("Chart 2")
# axs[1, 0].set_title("Chart 3")
# axs[1, 1].set_title("Chart 4")

# plt.tight_layout()  # To improve spacing between subplots

# # Show the final grid chart
# plt.show()

# # %%

# %%
