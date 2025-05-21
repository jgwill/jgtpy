from . import JGTCDS as cds

instrument="EUR/USD"
timeframe = "D1"
c=cds.create(instrument,timeframe,quiet=True)
print(c)
c.to_csv("../test/output-cds-231109a.csv")

