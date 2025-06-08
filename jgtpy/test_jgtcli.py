import unittest
from unittest.mock import patch
from io import StringIO

from jgtcli import main


class MockArgs:
    def __init__(self,
                 instrument="EUR/USD",
                 timeframe="H4",
                 tlidrange=None,
                 verbose=2,
                 quotescount=335,
                 ads=False,
                 full=False,
                 fresh=True,
                 gator_oscillator_flag=False,
                 mfi_flag=False,
                 balligator_flag=False,
                 balligator_period_jaws=89,
                 largest_fractal_period=89,
                 talligator_flag=False,
                 talligator_period_jaws=377,
                 viewpath=False,
                 dropna_volume=False,
                 quiet=False,
                 datefrom=None,
                 dateto=None):
        self.instrument = instrument
        self.timeframe = timeframe
        self.tlidrange = tlidrange
        self.verbose = verbose
        self.quotescount = quotescount
        self.ads = ads
        self.full = full
        self.fresh = fresh
        self.gator_oscillator_flag = gator_oscillator_flag
        self.mfi_flag = mfi_flag
        self.balligator_flag = balligator_flag
        self.balligator_period_jaws = balligator_period_jaws
        self.largest_fractal_period = largest_fractal_period
        self.talligator_flag = talligator_flag
        self.talligator_period_jaws = talligator_period_jaws
        self.viewpath = viewpath
        self.dropna_volume = dropna_volume
        self.quiet = quiet
        self.datefrom = datefrom
        self.dateto = dateto


class TestMain(unittest.TestCase):
    @patch("jgtcli._parse_args")
    @patch("jgtcli.createCDS_for_main")
    @patch("jgtcli.print_quiet")
    def test_main_invokes_create_cds(self, mock_print_quiet, mock_create_cds, mock_parse_args):
        # Arrange
        args = MockArgs()
        mock_parse_args.return_value = args

        # Act
        with patch("sys.stdout", new=StringIO()) as fake_out:
            main()

        # Assert
        mock_parse_args.assert_called_once()
        mock_print_quiet.assert_any_call(False, "Getting for : EUR/USD_H4")
        called_args, called_kwargs = mock_create_cds.call_args
        self.assertEqual(called_args[0], "EUR/USD")
        self.assertEqual(called_args[1], "H4")
        self.assertEqual(called_kwargs["verbose_level"], 2)
        self.assertEqual(called_kwargs["quotescount"], 335)
        self.assertIn("Processing CDS", fake_out.getvalue())


if __name__ == "__main__":
    unittest.main()
