# jgtfxc.py

import os
import platform

import json
#import datetime
from datetime import datetime
import pandas as pd



# origin_work_dir = os.getcwd()
# here = os.path.abspath(os.path.dirname(__file__))
# print("-----------------------------")
# print(here)
# print("-----------------------------")

# path_forexconnect = os.path.join(here, "forexconnect")

# if platform.system() == 'Windows':
#     path_forexconnect = os.path.join(here, 'lib', 'windows', 'mylib.dll')
# elif platform.system() == 'Linux':
#     path_forexconnect = os.path.join(here, 'lib', 'linux', 'mylib.so')
# else:
#     raise RuntimeError('Unsupported platform')


# os.chdir(path_forexconnect)

# from forexconnect import ForexConnect, fxcorepy
if platform.system() == 'Windows':
    from forexconnect import ForexConnect, fxcorepy
else: 
    if platform.system() == 'Linux':
        from jgtpy.forexconnect import ForexConnect, fxcorepy



# os.chdir(origin_work_dir)   

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
session=None
session_status=None
def get_session_status():
    return jgtfxcommon.get_connection_status()

def login_forexconnect(user_id, password, url, connection):
    global session,fx    
    fx = ForexConnect()
    try:
        fx.login(user_id, password, url, connection, "", "", jgtfxcommon.session_status_changed)
        session_status= jgtfxcommon.get_connection_status()
    except Exception as e:
        jgtfxcommon.print_exception(e)
    return fx

#@STCIssue Matching our original connect
def connect(quiet=True):
    global fx,quotes_count
    
    if fx is not None or jgtfxcommon.get_connection_status()== "CONNECTED":
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
        fx=None
        session_status= jgtfxcommon.get_connection_status()
        return True
    except Exception as e:
        jgtfxcommon.print_exception(e)
        fx=None
        return False
def disconnect(quiet=True):
    global fx
    if fx is None:
        print("Not connected")
        return True
    return logout_forexconnect(fx)


def status(quiet=True):
    return get_session_status()
    # if session is None:
    #     print_quiet(quiet,"UNKNOWN STATUS...")
    #     return False
    # else :
    #     print("---------AO2GSessionStatus-----------")
    #     print(fxcorepy.AO2GSessionStatus)
    #     print(session.AO2GSessionStatus)
    #     print("--------------------")
    #     if session.getStatus() == fxcorepy.AO2GSessionStatus.CONNECTED:
    #         print_quiet(quiet,"CONNECTED...")
    #         return True
    #     if session.getStatus() == fxcorepy.AO2GSessionStatus.DISCONECTED:
    #         print_quiet(quiet,"DISCONNECTED...")
    #         return False
    # print_quiet(quiet,"UNKNOWN STATUS...")
    # return False
        
def status1(quiet=True):
    global fx
    if fx is None:
        print_quiet(quiet,"STATUS : Not Connected")
        return False
    print_quiet(quiet,"STATUS : Connected")
    return True

def print_quiet(quiet,content):
    if not quiet:
        print(content)

def readconfig():
    # # Try reading config file from current directory
    # config_file = 'config.json'
    # if not os.path.isfile(config_file):
    #     # If config file not found, check home directory
    #     home_dir = os.path.expanduser("~")
    #     config_file = os.path.join(home_dir, 'config.json')

    # # Read config file
    # with open(config_file, 'r') as file:
    config = jgtfxcommon.readconfig()
    return config


def get_price_history(instrument, timeframe, datefrom=None, dateto=None,quotes_count_spec=None,quiet=True):
    global quotes_count,fx

    if quotes_count_spec is None:
        quotes_count_spec=quotes_count

    connect(quiet=quiet)
     

    try:
        if not quiet:
            print("")
            print("Requesting a price history...")

        if datefrom is not None:
            date_from_parsed = parse_date(datefrom)
        else:
            date_from_parsed=None
        
        if dateto is None:
            date_to_parsed = datetime.now()   
        else:
            date_to_parsed = parse_date(dateto)

        history = fx.get_history(instrument, timeframe, date_from_parsed, date_to_parsed, quotes_count_spec)

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
        dateto = datetime.now()

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




def parse_date(date_str):
    if date_str is None:
        for fmt in ('%d.%m.%Y %H:%M:%S', '%d.%m.%Y %H:%M','%d.%m.%Y','%Y%m%d%H%M','%y%m%d%H%M','%Y-%m-%d %H:%M'):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                pass
        raise ValueError('no valid date format found')