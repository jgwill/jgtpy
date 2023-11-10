# jgtfxc.py

import os
import json
import datetime
import pandas as pd
from forexconnect import ForexConnect, fxcorepy

#@STCGoal Future use
#import forexconnect as fxcon
# fxcon.ForexConnect.create_order_request
# fxcon.ForexConnect.create_request
# fxcon.ForexConnect.get_table
# fxcon.ForexConnect.get_timeframe
# fxcon.ForexConnect.get_timeframe

# from . import common_samples as jgtfxcommon
from . import jgtfxcommon


fx=None
quotes_count=None
stayConnected=False

def login_forexconnect(user_id, password, url, connection):
    fx = ForexConnect()
    try:
        fx.login(user_id, password, url, connection, "", "", jgtfxcommon.session_status_changed)
    except Exception as e:
        jgtfxcommon.print_exception(e)
    return fx

#@STCIssue Matching our original connect
def connect(quiet=True):
    global fx,quotes_count
    if fx is not None:
        if not quiet:
            print("Already connected")
        return
    
    config=readconfig()

    str_user_id = config['user_id']
    str_password = config['password']
    str_url = config['url']
    str_connection = config['connection']
    quotes_count = config['quotes_count']

    fx = login_forexconnect(str_user_id, str_password, str_url, str_connection)


def logout_forexconnect(fx):
    try:
        fx.logout()
    except Exception as e:
        jgtfxcommon.print_exception(e)
def disconnect(quiet=False):
    global fx
    if fx is None:
        print("Not connected")
        return
    logout_forexconnect(fx)
    fx=None

def status():
    global fx
    if fx is None:
        print("STATUS : Not connected")
        return
    print("STATUS : Connected")


def readconfig():
    # Try reading config file from current directory
    config_file = 'config.json'
    if not os.path.isfile(config_file):
        # If config file not found, check home directory
        home_dir = os.path.expanduser("~")
        config_file = os.path.join(home_dir, 'config.json')

    # Read config file
    with open(config_file, 'r') as file:
        config = json.load(file)
        return config


def get_price_history(instrument, timeframe, datefrom=None, dateto=None,quotes_count_spec=None,quiet=True):
    global quotes_count,fx

    if quotes_count_spec is None:
        quotes_count_spec=quotes_count

    connect()
    if dateto is None:
        dateto = datetime.datetime.now()    

    try:
        if not quiet:
            print("")
            print("Requesting a price history...")
        history = fx.get_history(instrument, timeframe, datefrom, dateto, quotes_count_spec)

        current_unit, _ = ForexConnect.parse_timeframe(timeframe)

        if current_unit == fxcorepy.O2GTimeFrameUnit.TICK:
            data = pd.DataFrame(history, columns=['Date', 'Bid', 'Ask'])
        else:
            data = pd.DataFrame(history, columns=['Date','BidOpen','BidHigh','BidLow','BidClose','AskOpen','AskHigh','AskLow','AskClose','Volume'])

        return data

    finally:
        if not stayConnected:
            disconnect()
        else:
            print("---we stay connected---")
        #logout_forexconnect(fx)


def get_price_history1(instrument, timeframe, datefrom=None, dateto=None):
    # Try reading config file from current directory
    config=readconfig()

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

        if current_unit == fxcorepy.O2GTimeFrameUnit.TICK:
            data = pd.DataFrame(history, columns=['Date', 'Bid', 'Ask'])
        else:
            data = pd.DataFrame(history, columns=['Date', 'BidOpen', 'BidHigh', 'BidLow', 'BidClose', 'Volume'])

        return data

    finally:
        logout_forexconnect(fx)


def get_price_history_printed(instrument, timeframe, datefrom=None, dateto=None):
    data = get_price_history(instrument, timeframe, datefrom, dateto)

    if data is not None:
        if 'Ask' in data.columns:
            print("Date, Bid, Ask")
        else:
            print("Date, BidOpen, BidHigh, BidLow, BidClose, Volume")

        for index, row in data.iterrows():
            values = row.values.tolist()
            print(",".join(str(value) for value in values))


# Example usage
#get_price_history_printed(instrument='EUR/USD', timeframe='m1')

#fx
def getAccount():
    account = fx.getAccount()
    print(account)
    return account

def getSubscribedSymbols():
    symbols = fx.getSubscribedSymbols()
    print(symbols)
    return symbols