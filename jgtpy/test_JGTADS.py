# import unittest
# from unittest.mock import patch
# import os

# import json
# import sys
# import pandas as pd

# #sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# from JGTADS import prepare_cds_for_ads_data

# class TestPrepareCdsForAdsData(unittest.TestCase):
#     @patch("JGTADS.pds.getPH")
#     @patch("JGTADS.cds.createFromDF")
#     def test_prepare_cds_for_ads_data(self, mock_createFromDF, mock_getPH):
#         # Arrange
#         instrument = "EUR/USD"
#         timeframe = "H1"
#         nb_bar_on_chart = 400
#         recreate_data = True

#         # Mock the return values of the dependencies
#         mock_getPH.return_value = pd.DataFrame()  # Replace with your desired DataFrame
#         mock_createFromDF.return_value = pd.DataFrame()  # Replace with your desired DataFrame

#         # Act
#         result = prepare_cds_for_ads_data(instrument, timeframe, nb_bar_on_chart, recreate_data)

#         # Assert
#         mock_getPH.assert_called_once_with(instrument, timeframe, nb_bar_on_chart)
#         mock_createFromDF.assert_called_once()  # Add any necessary assertions for the createFromDF function
#         self.assertEqual(result, mock_createFromDF.return_value)  # Add any necessary assertions for the result

#     @patch("JGTADS.pds.getPH")
#     @patch("JGTADS.cds.createFromDF")
#     def test_prepare_cds_for_ads_data_with_cache(self, mock_createFromDF, mock_getPH):
#         # Arrange
#         instrument = "EUR/USD"
#         timeframe = "H1"
#         nb_bar_on_chart = 400
#         recreate_data = False

#         # Mock the return values of the dependencies
#         mock_getPH.return_value = pd.DataFrame()  # Replace with your desired DataFrame
#         mock_createFromDF.return_value = pd.DataFrame()  # Replace with your desired DataFrame

#         # Act
#         result = prepare_cds_for_ads_data(instrument, timeframe, nb_bar_on_chart, recreate_data)

#         # Assert
#         mock_getPH.assert_not_called()  # The getPH function should not be called
#         mock_createFromDF.assert_called_once()  # Add any necessary assertions for the createFromDF function
#         self.assertEqual(result, mock_createFromDF.return_value)  # Add any necessary assertions for the result

# if __name__ == "__main__":
#     unittest.main()