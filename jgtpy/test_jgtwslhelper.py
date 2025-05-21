# import unittest
# from unittest.mock import patch
# from datetime import datetime

# import sys
# import os

# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# from jgtutils.jgtwslhelper import _mkbash_cmd_string_jgtfxcli_range,resolve_cli_path


# class TestMkBashCmdStringJgtfxcliRange(unittest.TestCase):
#     @patch("jgtwslhelper.resolve_cli_path")
#     @patch("jgtwslhelper.jgtcommon.tlid_range_to_jgtfxcon_start_end_str")
#     def test_mkbash_cmd_string_jgtfxcli_range(
#         self, mock_tlid_range_to_jgtfxcon_start_end_str, mock_resolve_cli_path
#     ):
#         # Arrange
#         instrument = "EUR/USD"
#         timeframe = "H1"
#         tlid_range = "2101010000_2101012359"
#         cli_path = resolve_cli_path()
#         verbose_level = 2
#         date_from = "20220101"
#         date_to = "20220101"

#         #mock_resolve_cli_path.return_value = cli_path
#         mock_tlid_range_to_jgtfxcon_start_end_str.return_value = (date_from, date_to)

#         expected_bash_command = f'pwd;{cli_path} -i "{instrument}" -t "{timeframe}" -s {date_from} -e {date_to} -v {verbose_level}'

#         # Act
#         result = _mkbash_cmd_string_jgtfxcli_range(
#             instrument, timeframe, tlid_range, cli_path, verbose_level
#         )

#         # Assert
#         mock_resolve_cli_path.assert_called_once_with(cli_path)
#         mock_tlid_range_to_jgtfxcon_start_end_str.assert_called_once_with(tlid_range)
#         self.assertEqual(result, expected_bash_command)


# if __name__ == "__main__":
#     unittest.main()
