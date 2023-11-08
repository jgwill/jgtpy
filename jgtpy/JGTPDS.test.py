# main.py

import JGTPDS as pds

pds.stayConnected=True


d=pds.getPH('EUR/USD', 'H4')
d.to_csv('../EURUSD_H4b.csv')
print(d)

pds.status()

d=pds.getPH('AUD/USD', 'H4')
d.to_csv('../AUDUSD_H4b.csv')
print(d)



pds.status()
