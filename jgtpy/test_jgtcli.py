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
        # additional attributes expected by jgtcli.main
        self.quiet = False
        self.full = False
        self.fresh = True
        self.gator_oscillator_flag = False
        self.mfi_flag = True
        self.balligator_flag = False
        self.balligator_period_jaws = 89
        self.largest_fractal_period = 89
        self.talligator_flag = False
        self.talligator_period_jaws = 377
        self.viewpath = False
        self.dropna_volume = True


class TestMain(unittest.TestCase):
    @patch("jgtcli._parse_args")
    @patch("jgtcli.createCDS_for_main")
    @patch("jgtcli.print_quiet")
    def test_main(self, mock_print_quiet, mock_create, mock_parse_args):
        args = MockArgs()
        mock_parse_args.return_value = args

        with patch("sys.stdout", new=StringIO()) as fake_out:
            main()

        mock_parse_args.assert_called_once()
        mock_print_quiet.assert_called_once_with(False, "Getting for : EUR/USD_H4")
        mock_create.assert_called_once()
        call_args = mock_create.call_args[0]
        self.assertEqual(call_args[0], "EUR/USD")
        self.assertEqual(call_args[1], "H4")
        self.assertEqual(fake_out.getvalue(), "Processing CDS\nDropping NA Volume\n")


if __name__ == "__main__":
    unittest.main()
