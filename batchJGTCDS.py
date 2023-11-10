import jgtpy.JGTPDS as pds
import jgtpy.JGTIDS as ids
import jgtpy.JGTCDS as cds
import os
instrument="AUD/USD"
timeframe = "D1"
c=cds.create(instrument,timeframe,nb2retrieve=3000,stayConnected=False,quiet=True)
print(c)

# Define the file path based on the environment variable or local path
data_path = os.environ.get('JGTPY_DATA', './data')

c.to_csv(data_path+"/"+ instrument.replace('/','-') + '_' + timeframe + '.cds.csv')

