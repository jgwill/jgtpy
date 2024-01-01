# import unittest
# import pandas as pd
# from unittest.mock import patch

# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
# from jgtutils import jgtconstants as c
# from jgtpy.JGTIDS import ids_add_indicators

# import jgtpy.testmock_IDS as mk

# class TestIdsAddIndicators(unittest.TestCase):
#     def test_ids_add_indicators_use_legacy(self):
#         # Arrange
#         dfsrc = mk.pds_SPX500_H4
#         dfsrc = dfsrc.set_index('Date')  # Set index to 'Date' column
#         #pd.DataFrame({'Date': ['2022-01-01', '2022-01-02', '2022-01-03'],
#                             #   'Open': [100, 200, 300],
#                             #   'High': [150, 250, 350],
#                             #   'Low': [50, 150, 250],
#                             #   'Close': [120, 220, 320]})
#         #dfsrc = pd.read_csv()
#         enableGatorOscillator = False
#         enableMFI = False
#         dropnavalue = True
#         quiet = True
#         cleanupOriginalColumn = True
#         useLEGACY = True

#         # Act
#         result = ids_add_indicators(dfsrc, enableGatorOscillator, enableMFI, dropnavalue, quiet, cleanupOriginalColumn, useLEGACY)
#         #result = result.set_index('Date')  # Set index to 'Date' column
#         dfc = mk.cds_SPX500_H4
#         dfc = dfc.set_index('Date')
        
#         itst = result[['Date'] == '2023-12-11 18:00:00']
#         ctst = dfc[['Date'] == '2023-12-11 18:00:00']

#         # Assert
#         # Add your assertions here to verify the result
        
#         #result.to_csv("testoutput.csv")
#         #,Date,Volume,Open,High,Low,Close,Median,ac,jaw,teeth,lips,bjaw,bteeth,blips,ao,fh,fl,fh3,fl3,fh5,fl5,fh8,fl8,fh13,fl13,fh21,fl21,fh34,fl34,fh55,fl55,fh89,fl89,jaws_tmp,teeth_tmp,lips_tmp,fdbb,fdbs,fdb,aof,aoaz,aobz,zlc,zlcb,zlcs,zcol,sz,bz,acs,acb,ss,sb
#         #Date,Volume,Open,High,Low,Close,Median,ac,jaw,teeth,lips,bjaw,bteeth,blips,ao,fh,fl,fh3,fl3,fh5,fl5,fh8,fl8,fh13,fl13,fh21,fl21,fh34,fl34,fh55,fl55,fh89,fl89,jaws_tmp,teeth_tmp,lips_tmp
#         #2023-12-11 18:00:00,9025,4612.98,4625.38,4610.11,4624.13,4617.745,3.2750529412,4570.9229811635,4581.8696910259,4593.4831435394,4429.7354803861,4501.253756322,4548.2185121858,29.0130147059,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,4594.4615849937,4601.5309294922,4607.6369896031
#         #443,2023-12-11 18:00:00,9025,4612.98,4625.38,4610.11,4624.13,4617.745,3.2750529412,4570.9229811635,4581.8696910259,4593.4831435394,4429.7354803861,4501.253756322,4548.2185121858,29.0130147059,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4594.4615849937,4601.5309294922,4607.6369896031,0.0,0.0,0.0,0.0,1,0,0.0,0.0,0.0,gray,0.0,0.0,1.0,0.0,0.0,0.0
        

    
# if __name__ == "__main__":
#     unittest.main()

    
