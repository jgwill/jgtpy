import jgtpy.JGTPDS as pds
import jgtpy.JGTIDS as ids

d=pds.getPH("AUD/USD","W1")
print(d)
ofn="AUD-USD_W1_noindex.csv"
d.to_csv(ofn,index=False)
print("Output:")
print(ofn)

ofn="AUD-USD_W1_index.csv"
d.to_csv(ofn,index=True)
print("Output:")
print(ofn)
