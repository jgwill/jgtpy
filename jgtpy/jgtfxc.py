# jgtfxc.py

import os
import platform

import json
#import datetime
from datetime import datetime,timezone
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
        try:
            # Try to import ForexConnect and fxcorepy from jgtpy.forexconnect
            from jgtpy.forexconnect import ForexConnect, fxcorepy
        except ModuleNotFoundError:
            # If that fails, try to import them directly
            try:
                from .forexconnect import ForexConnect, fxcorepy
            except ModuleNotFoundError:
                # If that also fails, print an error message
                print("Could not import ForexConnect or fxcorepy. Please ensure the modules are installed and available.")



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

def login_forexconnect(user_id, password, url, connection, quiet=False):
    global session,fx    
    jgtfxcommon.quiet=quiet
    fx = ForexConnect()
    try:
        fx.login(user_id, password, url, connection, "", "", jgtfxcommon.session_status_changed)
        session_status= jgtfxcommon.get_connection_status()
    except Exception as e:
        jgtfxcommon.print_exception(e)
    return fx
config=None
#@STCIssue Matching our original connect
def connect(quiet=True,json_config_str=None):
    global fx,quotes_count,config
    
    if fx is not None or jgtfxcommon.get_connection_status()== "CONNECTED":
        if not quiet:
            print("Already connected")
        return
    
    if config is None:
        config=readconfig(json_config_str)

    str_user_id = config['user_id']
    str_password = config['password']
    str_url = config['url']
    str_connection = config['connection']
    quotes_count = config['quotes_count']

    fx = login_forexconnect(str_user_id, str_password, str_url, str_connection,quiet=quiet)


def logout_forexconnect(fx,quiet=False):
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
        print_quiet(quiet,"Not connected")
        return True
    return logout_forexconnect(fx,quiet)


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
config=None
def readconfig(json_config_str=None):
    global config
    # # Try reading config file from current directory
    # config_file = 'config.json'
    # if not os.path.isfile(config_file):
    #     # If config file not found, check home directory
    #     home_dir = os.path.expanduser("~")
    #     config_file = os.path.join(home_dir, 'config.json')

    # # Read config file
    # with open(config_file, 'r') as file:
    if config is None:
        config = jgtfxcommon.readconfig(json_config_str)
    return config


def get_price_history(instrument, timeframe, datefrom=None, dateto=None,quotes_count_spec=None,quiet=True):
    global quotes_count,fx

    if quotes_count_spec is None:
        quotes_count_spec=quotes_count

    connect(quiet=quiet)
     

    try:
        print_quiet(quiet,"Requesting a price history...")
  

        if datefrom is not None:
            date_from_parsed = parse_date(datefrom)
        else:
            date_from_parsed=None
        
        if dateto is None:
            date_to_parsed = datetime.now(timezone.utc)
        else:
            date_to_parsed = parse_date(dateto)
        
        if not quiet:
            print("Date from : " + str(date_from_parsed))
            print("Date to : " + str(date_to_parsed))


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