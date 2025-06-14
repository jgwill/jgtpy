import unittest
from unittest.mock import patch
from io import StringIO

from jgtcli import main


class MockArgs:
    def __init__(self, instrument="EUR/USD", timeframe="H4", tlidrange=None, verbose=2, quotescount=335, ads=False, compress=False, datefrom=None, dateto=None):
        self.instrument = instrument
        self.timeframe = timeframe
        self.tlidrange = tlidrange
        self.verbose = verbose
        self.quotescount = quotescount
        self.ads = ads
        self.compress = compress
        self.datefrom = datefrom
        self.dateto = dateto


class TestMain(unittest.TestCase):
    @patch("jgtcli.parse_args")
    @patch("jgtcli.createCDS_for_main")
    @patch("jgtcli.print_quiet")
    def test_main(self, mock_print_quiet, mock_create, mock_parse_args):
        args = MockArgs()
        mock_parse_args.return_value = args

        with patch("sys.stdout", new=StringIO()) as fake_out:
            main()

        mock_parse_args.assert_called_once()
        mock_print_quiet.assert_called_once_with(False, "Getting for : EUR/USD_H4")
        mock_create.assert_called_once_with("EUR/USD", "H4", False, 2, None, False, None, quotes_count=335)
        self.assertEqual(fake_out.getvalue(), "Processing CDS\n")


if __name__ == "__main__":
    unittest.main()
