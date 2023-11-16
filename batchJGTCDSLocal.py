import jgtpy.JGTPDS as pds
import jgtpy.JGTIDS as ids
import jgtpy.JGTCDS as cds
import os

# List of columns to remove
columns_to_remove = ['aofvalue', 'aofhighao', 'aoflowao', 'aofhigh', 'aoflow', 'aocolor', 'accolor','fdbbhigh','fdbblow','fdbshigh','fdbslow']

# Define the file path based on the environment variable or local path
data_path_cds = cds.get_data_path()


instrument="EUR/USD"
timeframe = "D1"

#H1 H4 D1 m15 m5 W1;do for i in "EUR/USD" "AUD/USD" "USD/CAD" "GBP/USD" "SPX500"
instruments = ["USD/CAD", "EUR/USD", "GBP/USD", "AUD/USD","NAS100"]
instruments = ["USD/CAD", "EUR/USD", "GBP/USD", "AUD/USD","SPX500"]

timeframes = ["W1","D1", "H4", "H1", "m15","m5"]
timeframes = ["H1","W1","D1", "H4", "m15"]
#timeframes = ["M1"]


for timeframe in timeframes:
  
  for instrument in instruments:
    print("Doing CDS for : " + instrument + "_" + timeframe)
    c=cds.createFromPDSFile(instrument,timeframe)
    # Remove the specified columns
    c = c.drop(columns=columns_to_remove, errors='ignore')
    
    fpath=pds.mk_fullpath(instrument,timeframe,'csv',data_path_cds)
    c.to_csv(fpath)
