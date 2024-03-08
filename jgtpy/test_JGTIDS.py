

    
import unittest
import pandas as pd
from JGTIDS import tocds
from jgtpy.JGTADSRequest import JGTADSRequest
from jgtpy.JGTChartConfig import JGTChartConfig
import os

class TestJGTIDS(unittest.TestCase):
  
    def test_tocds(self):

        i="SPX500"
        t="H4"
        ifn=i.replace("/","-")
        
        # Arrange
        try:        dfsrc = pd.read_csv(f"samples/{ifn}_{t}.csv")# mk.pds_SPX500_H4
        except:
          dfsrc = pd.read_csv("../samples/SPX500_H4.csv")# mk.pds_SPX500_H4
        dfsrc = dfsrc.set_index('Date')  # Set index to 'Date' column
        quiet = True
        peak_distance = 13
        peak_width = 8
        cc = JGTChartConfig()
        cc.nb_bar_on_chart = 302
        rq= JGTADSRequest()
        rq.peak_distance = peak_distance
        rq.peak_width = peak_width
        rq.peak_divider_min_height = 3

        # Act
        result = tocds(dfsrc, quiet=quiet, cc=cc,rq=rq)

        # Assert
        # Add your assertions here to verify the result

        # Example assertion:
        #self.assertEqual(len(result), len(dfsrc))  # Verify that the result has the same length as the input dataframe

        # You can add more assertions to validate the output

        len_res=len(result)
        self.assertGreaterEqual(len_res, cc.nb_bar_on_chart)  # Verify that the result has the same length as the input dataframe
        # Example assertion:
        self.assertTrue(all(result['Close'] >= 0))  # Verify that all 'Close' values are non-negative

        # You can add more assertions based on your specific requirements


if __name__ == "__main__":
    unittest.main()