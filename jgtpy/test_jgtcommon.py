import unittest
import datetime
from jgtutils.jgtos import tlid_range_to_jgtfxcon_start_end_str
from jgtutils.jgtos import tlid_range_to_start_end_datetime

class TestTlidRangeToJgtfxconStartEndStr(unittest.TestCase):
    def test_tlid_range_to_jgtfxcon_start_end_str(self):
        # Arrange
        tlid_range = "211124_220113"
        expected_start = '11.24.2021 00:00:00'
        expected_end = '01.13.2022 00:00:00'

        # Act
        result_start, result_end = tlid_range_to_jgtfxcon_start_end_str(tlid_range)

        # Assert
        self.assertEqual(str(result_start), expected_start)
        self.assertEqual(str(result_end), expected_end)
        
        
        tlid_range = "2111242222_2201132323"
        expected_start = '11.24.2021 22:22:00'
        expected_end = '01.13.2022 23:23:00'

        # Act
        result_start, result_end = tlid_range_to_jgtfxcon_start_end_str(tlid_range)

        # Assert
        self.assertEqual(result_start, expected_start)
        self.assertEqual(result_end, expected_end)
        
        
        
        tlid_range = "9611242222_0101132323"
        expected_start = '11.24.1996 22:22:00'
        expected_end = '01.13.2001 23:23:00'

        # Act
        result_start, result_end = tlid_range_to_jgtfxcon_start_end_str(tlid_range)

        # Assert
        self.assertEqual(str(result_start), expected_start)
        self.assertEqual(str(result_end), expected_end)





class TestTlidRangeToStartEndDatetime(unittest.TestCase):
    def test_tlid_range_to_start_end_datetime_with_time(self):
        # Arrange
        tlid_range = "2111242200_2201132359"
        expected_start = datetime.datetime(2021, 11, 24, 22, 0)
        expected_end = datetime.datetime(2022, 1, 13, 23, 59)

        # Act
        result_start, result_end = tlid_range_to_start_end_datetime(tlid_range)

        # Assert
        self.assertEqual(result_start, expected_start)
        self.assertEqual(result_end, expected_end)

    def test_tlid_range_to_start_end_datetime_with_date(self):
        # Arrange
        tlid_range = "2111240010_2201132359"
        expected_start = datetime.datetime(2021, 11, 24,0,10)
        expected_end = datetime.datetime(2022, 1, 13, 23, 59)

        # Act
        result_start, result_end = tlid_range_to_start_end_datetime(tlid_range)

        # Assert
        self.assertEqual(result_start, expected_start)
        self.assertEqual(result_end, expected_end)

    def test_tlid_range_to_start_end_datetime_invalid_format(self):
        # Arrange
        tlid_range = "992345_2201131122"
        expected_result = None

        # Act
        result = tlid_range_to_start_end_datetime(tlid_range)

        # Assert
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
