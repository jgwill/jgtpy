# %% imports
from matplotlib import pyplot as plt
import jgtpy as jgt

jgt.help()

# %% test

i = "SPX500"
t = "H4"


# %% ADS
print("Creating the ADS Chart...")
ads_chart, _ads_plt_arr, _ads_df = jgt.ads(i, t,show=False)
print("....done")
#ads_chart.show()

# %%
ads_chart.__dict__
# %% Serialize import pickle
import pickle
import mplfinance as mpf

# Save the Matplotlib figure using pickle
output_file_name = "figure_data2.pickle"
print("Saving the ADS Chart..." + output_file_name)
with open(output_file_name, "wb") as file:
    pickle.dump(ads_chart, file)
print("....done")

# %% Load it back
# Load the Matplotlib figure from the pickle file
print("Loading back the ADS Chart..." + output_file_name)
with open(output_file_name, "rb") as file:
    loaded_pickle_mplfinance = pickle.load(file)

loaded_pickle_mplfinance._mouseover = True

# Recreate the plot object using the figure attribute from the restored object
#recreated_plot = mpf.plot(loaded_pickle_mplfinance.figure)

# Display the loaded figure
# plt.figure(loaded_figure.number)
# plt.figure


# %%
