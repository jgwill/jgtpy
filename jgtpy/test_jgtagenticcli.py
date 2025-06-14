import unittest
from unittest.mock import patch
from io import StringIO

from jgtagenticcli import main, parse_args

class TestAgenticCli(unittest.TestCase):
    @patch('jgtagenticcli.scan_fdb')
    @patch('jgtagenticcli.parse_args')
    def test_cli_invokes_scan(self, mock_parse, mock_scan):
        mock_parse.return_value = parse_args([])
        mock_scan.return_value = [{'instrument': 'EUR/USD', 'timeframe': 'H1', 'fdb': True}]
        with patch('sys.stdout', new=StringIO()) as fake:
            main()
        mock_scan.assert_called_once()
        self.assertIn('EUR/USD_H1', fake.getvalue())

if __name__ == '__main__':
    unittest.main()
