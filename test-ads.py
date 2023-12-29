# %% Import packages
from jgtpy import JGTADS as ads
from jgtpy import JGTPDSP as pds
from jgtpy import JGTChartConfig 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
print(os.getenv("JGTPY_DATA"))

instrument = "XAU/USD"
instrument = "SPX500"
instrument = "EUR/USD"
# %% Load data and plot all in one operation
show=True
#m1p=pds.getPH(instrument, "M1")

#%% Plot all charts in one operation
cc = JGTChartConfig.JGTChartConfig()
cc.saucer_marker_size = 14;cc.ac_signals_marker_size=14
cc.fig_ratio_x = 24
cc.fig_ratio_y = 16
cc.nb_bar_on_chart = 340
cc.plot_style = "yahoo"

#M1c, M1a = ads.plot_from_pds_df(m1p,instrument, "M1", show=show)
M1, M1a = ads.plot(instrument, "M1", show=show,cc=cc)

w1, w1a = ads.plot(instrument, "W1", show=show,cc=cc)
d1, d1a = ads.plot(instrument, "D1", show=show,cc=cc)

h4, h4a = ads.plot(instrument, "H4", show=show,cc=cc)
h1, h1a = ads.plot(instrument, "H1", show=show,cc=cc)
m15, m15a = ads.plot(instrument, "m15", show=show,cc=cc)

#%% m5
m5, m15a = ads.plot(instrument, "m5", show=show,cc=cc)

#%% Save charts
M1.savefig("M1.png")
w1.savefig("w1.png")
d1.savefig("d1.png")
h4.savefig("h4.png")
h1.savefig("h1.png")
m15.savefig("m15.png")
m5.savefig("m5.png")
#mi1,mi1a = ads.plot(instrument, "m1", show=show)

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
