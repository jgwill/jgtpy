import jgtpy.JGTPDS as pds
import jgtpy.JGTIDS as ids

d=pds.getPH("AUD/USD","W1")
i=ids.tocds(d)
print(i)
ofn="AUD-USD_W1_noindex.ids.csv"
i.to_csv(ofn,index=False)
print("Output:")
print(ofn)

ofn="AUD-USD_W1_index.ids.csv"
i.to_csv(ofn,index=True)
print("Output:")
print(ofn)
