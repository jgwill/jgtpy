# main.py

import jgtpy.JGTPDS as pds

pds.stayConnected=True


d=pds.getPH('EUR/USD', 'H4')
d.to_csv('../test/EURUSD_H4_noindex.csv',index=False)
d.to_csv('../test/EURUSD_H4_index.csv',index=True)
print(d)

pds.status()

d=pds.getPH('AUD/USD', 'H4')
d.to_csv('../test/AUDUSD_H4_noindex.csv',index=False)
d.to_csv('../test/AUDUSD_H4_index.csv',index=True)
print(d)



pds.status()
