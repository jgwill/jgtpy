import jgtpy.JGTPDS as pds
import jgtpy.JGTIDS as ids
import jgtpy.JGTCDS as cds
import os
instrument="EUR/USD"
timeframe = "D1"
c=cds.createFromPDSFile(instrument,timeframe)
print(c)

# Assuming you already have a DataFrame named df
# Replace this with your actual DataFrame creation or loading code

# List of columns to remove
columns_to_remove = ['aofvalue', 'aofhighao', 'aoflowao', 'aofhigh', 'aoflow', 'aocolor', 'accolor','fdbbhigh','fdbblow','fdbshigh','fdbslow']

# Remove the specified columns
c = c.drop(columns=columns_to_remove, errors='ignore')


# Define the file path based on the environment variable or local path
data_path = os.environ.get('JGTPY_DATA', './data')
data_path=os.path.join(data_path,'cds')
fpath=pds.mk_fullpath(instrument,timeframe,'csv',data_path)
c.to_csv(fpath)