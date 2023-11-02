# jgtfxc.py

import json
import datetime
import pandas as pd
from forexconnect import ForexConnect, fxcorepy

import common_samples
# as common_samples


def get_price_history(instrument, timeframe, datefrom=None, dateto=None):
    # Read config file
    with open('config.json', 'r') as file:
        config = json.load(file)

    str_user_id = config['user_id']
    str_password = config['password']
    str_url = config['url']
    str_connection = config['connection']
    quotes_count = config['quotes_count']

    if dateto is None:
        dateto = datetime.datetime.now()

    with ForexConnect() as fx:
        try:
            fx.login(str_user_id, str_password, str_url,
                     str_connection, "", "",
                     common_samples.session_status_changed)

            print("")
            print("Requesting a price history...")
            history = fx.get_history(instrument, timeframe, datefrom, dateto, quotes_count)
            current_unit, _ = ForexConnect.parse_timeframe(timeframe)

            date_format = '%m.%d.%Y %H:%M:%S'
            if current_unit == fxcorepy.O2GTimeFrameUnit.TICK:
                print("Date, Bid, Ask")
                print(history.dtype.names)
                for row in history:
                    print("{0:s}, {1:,.5f}, {2:,.5f}".format(
                        pd.to_datetime(row['Date']).strftime(date_format), row['Bid'], row['Ask']))
            else:
                print("Date, BidOpen, BidHigh, BidLow, BidClose, Volume")
                for row in history:
                    dt = pd.to_datetime(row['Date']).strftime(date_format)
                    o = row['BidOpen']
                    h = row['BidHigh']
                    l = row['BidLow']
                    c = row['BidClose']
                    v = row['Volume']

                    print("{0:s}, {1:,.5f}, {2:,.5f}, {3:,.5f}, {4:,.5f}, {5:d}".format(
                        dt, o, h, l, c, v))
        except Exception as e:
            common_samples.print_exception(e)
        try:
            fx.logout()
        except Exception as e:
            common_samples.print_exception(e)