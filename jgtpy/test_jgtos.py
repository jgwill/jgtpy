import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from jgtos import mk_fn


class TestMkFn(unittest.TestCase):
    def test_mk_fn(self):
        # Arrange
        instrument = "EUR/USD"
        timeframe = "H1"
        ext = "csv"
        expected_filename = "EUR-USD_H1.csv"

        # Act
        result = mk_fn(instrument, timeframe, ext)

        # Assert
        self.assertEqual(result, expected_filename)


if __name__ == "__main__":
    unittest.main()
