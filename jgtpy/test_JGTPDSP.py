    
import unittest
from datetime import datetime
from unittest.mock import patch

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTPDSP import create_filestore_path


class TestCreateFilestorePath(unittest.TestCase):
    @patch("JGTPDSP.jgtos.create_filestore_path")
    def test_create_filestore_path(self, mock_create_filestore_path):
        # Arrange
        mock_create_filestore_path.return_value = "/tmp/data/EUR-USD_H1_2101010000_2101012359.csv"
        instrument = "EUR/USD"
        timeframe = "H1"
        quiet = True
        compressed = False
        tlid_range = "2101010000_2101012359"
        output_path="/tmp/data"
        # Act
        result = create_filestore_path(
            instrument, timeframe, quiet, compressed, tlid_range,output_path=output_path
        )
        print(result)
        # Assert
        mock_create_filestore_path.assert_called_once_with(
            instrument, timeframe, quiet, compressed, tlid_range,output_path
        )
        self.assertEqual(result, "/tmp/data/EUR-USD_H1_2101010000_2101012359.csv")


from JGTPDSP import mk_fn_range, mk_fn

class TestMkFnRange(unittest.TestCase):
    def test_mk_fn_range(self):
        # Arrange
        instrument = "EUR/USD"
        timeframe = "H1"
        start = datetime(2022, 1, 1)
        end = datetime(2022, 1, 2)
        ext = "csv"

        # Act
        result = mk_fn_range(instrument, timeframe, start, end, ext)

        # Assert
        expected_result = "EUR-USD_H1_2201010000_2201020000.csv"
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()


