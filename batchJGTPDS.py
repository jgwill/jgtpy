import jgtpy.JGTPDS as pds
import jgtpy.JGTIDS as ids
import jgtpy.JGTCDS as cds
import os
instrument="AUD/USD"
timeframe = "D1"

# List of instruments
instruments = ["USD/CAD", "NAS100", "GBP/CAD", "EUR/USD", "GBP/USD", "AUD/USD"]
instruments = ["USD/CAD", "EUR/USD", "GBP/USD", "AUD/USD"]
#instruments = ["GBP/CAD"]

# Desired timeframe
timeframe = "m15"
# List of timeframes
timeframes = ["M1","W1","D1", "H4", "H1", "m15","m5"]
#timeframes = ["W1","D1", "H4", "H1", "m15","m5"]
#timeframes = ["M1"]
# Limit for the number of data points
limit = 750

pds.stayConnectedSetter(True)
# Iterate over instruments and fetch data

for timeframe in timeframes:
  l=limit
  if timeframe == "M1":
    l=500
  if timeframe == "W1":
    l=1500
  if timeframe == "D1":
    l=2500
  
  for instrument in instruments:
    if instrument == "GBP/CAD":
      l=350
    # Call the custom function to get data
    print("Doing: " + instrument + "_" + timeframe)
    f = pds.getPH_to_filestore(instrument, timeframe, l)
    print(f)

pds.disconnect()