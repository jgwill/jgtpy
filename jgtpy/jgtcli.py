import argparse
import sys
from .JGTPDS import getPH

def main(args=None):
    """Entry point for the command line application"""
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Fetch price history data")
    
    parser.add_argument("-i", "--instrument", required=True, help="Instrument symbol")
    parser.add_argument("-t", "--timeframe", required=True, help="Timeframe for the data")
    parser.add_argument("-f", "--from", dest="from_date", required=True, help="Start date for the data range")
    parser.add_argument("-to", "--to", dest="to_date", required=True, help="End date for the data range")

    args = parser.parse_args(args)

    df = getPH(args.instrument, args.timeframe, args.from_date, args.to_date)
    print(df)

if __name__ == "__main__":
    main()
