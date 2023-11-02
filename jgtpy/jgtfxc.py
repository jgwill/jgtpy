# jgtfxc.py

import os
import json
import datetime
import pandas as pd
from forexconnect import ForexConnect, fxcorepy

import common_samples_231025 as common_samples


def login_forexconnect(user_id, password, url, connection):
    fx = ForexConnect()
    try:
        fx.login(user_id, password, url, connection, "", "", common_samples.session_status_changed)
    except Exception as e:
        common_samples.print_exception(e)
    return fx


def logout_forexconnect(fx):
    try:
        fx.logout()
    except Exception as e:
        common_samples.print_exception(e)


def get_price_history(instrument, timeframe, datefrom=None, dateto=None):
    # Try reading config file from current directory
    config_file = 'config.json'
    if not os.path.isfile(config_file):
        # If config file not found, check home directory
        home_dir = os.path.expanduser("~")
        config_file = os.path.join(home_dir, 'config.json')

    # Read config file
    with open(config_file, 'r') as file:
        config = json.load(file)

    str_user_id = config['user_id']
    str_password = config['password']
    str_url = config['url']
    str_connection = config['connection']
    quotes_count = config['quotes_count']

    if dateto is None:
        dateto = datetime.datetime.now()

    fx = login_forexconnect(str_user_id, str_password, str_url, str_connection)

    try:
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
    finally:
        logout_forexconnect(fx)


# Example usage
#get_price_history(instrument='EUR/USD', timeframe='m1')