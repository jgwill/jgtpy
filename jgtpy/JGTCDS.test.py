from . import JGTCDS as cds

c=cds.create("EUR/USD","D1")
print(c)
c.to_csv("../test/output-cds-231109a.csv")

