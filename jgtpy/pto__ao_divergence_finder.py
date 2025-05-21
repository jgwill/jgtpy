"""
This Python code processes financial data stored in a pandas DataFrame named 'data'. It calculates the Awesome Oscillator (AO) using the median price and two simple moving averages (SMA). Then, it identifies peaks in both the AO and price data. The code defines a function to find divergences between the price and AO peaks based on a tolerance range. Finally, it outputs the detected divergences, specifying the corresponding indices of price and AO peaks.
"""
#%% imports
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from jgtpy import JGTPDSP as pds

#%% data
#data = pds.getPH("EUR/USD","H4",quiet=False)
data = pd.read_csv("Data.pds.csv")

#%% AO
# Assuming 'data' is a pandas DataFrame with 'High', 'Low' and 'Close' columns
# Calculate Awesome Oscillator (AO)
data['median_price'] = (data['High'] + data['Low']) / 2
data['sma_5'] = data['median_price'].rolling(window=5).mean()
data['sma_34'] = data['median_price'].rolling(window=34).mean()
data['ao'] = data['sma_5'] - data['sma_34']

output_filename = "ao_divergence_finder_data.csv"
data.to_csv(output_filename)

#%% Find peaks in AO
# Find peaks in AO
ao_peaks, _ = find_peaks(data['ao'])

# Find peaks in price
price_peaks, _ = find_peaks(data['Close'])

#%% Find divergences
# Define a function to find divergence
def find_divergences(price_peaks, ao_peaks, price, ao):
    divergences = []
    for peak_index in price_peaks:
        # Check if there is a corresponding peak in AO within a tolerance range
        ao_peak_index = np.where(np.abs(ao_peaks - peak_index) < tolerance)[0]
        if ao_peak_index.size > 0:
            price_peak_val = price.iloc[peak_index]
            ao_peak_val = ao.iloc[ao_peak_index[0]]
            if np.sign(price_peak_val) != np.sign(ao_peak_val):
                # Divergence found: record the indices of the price and AO peaks
                divergences.append((peak_index, ao_peak_index[0]))
    return divergences

# Set a tolerance for how close the peaks need to be
tolerance = 5  # Number of periods

# Find divergences
divergences = find_divergences(price_peaks, ao_peaks, data['Close'], data['ao'],)

# Output the divergences
for div in divergences:
    print(f"Divergence found between price index {div[0]} and AO index {div[1]}")

dfdiv = pd.DataFrame(divergences)
dfdiv.to_csv("ao_divergence_finder.div.csv")
