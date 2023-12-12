

 # OrderMonitor.py
# Copyright 2019 Gehtsoft USA LLC

# Licensed under the license derived from the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License.

# You may obtain a copy of the License at

# http://fxcodebase.com/licenses/open-source/license.html

# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List
from enum import Enum
import json
import os
import tlid

#------------------------#

# common.py


import logging
import datetime
import traceback
import argparse
import sys


try :
    import __main__
    logging.basicConfig(filename='{0}.log'.format(__main__.__file__), level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s', datefmt='%m.%d.%Y %H:%M:%S')
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)
except:
    print('logging failed - dont worry')

def add_main_arguments(parser: argparse.ArgumentParser):
    parser.add_argument('--login',
                        metavar="LOGIN",
                        required=True,
                        help='Your user name.')

    parser.add_argument('--password',
                        metavar="PASSWORD",
                        required=True,
                        help='Your password.')

    parser.add_argument('--urlserver',
                        metavar="URL",
                        required=True,
                        help='The server URL. For example,\
                                 https://www.fxcorporate.com/Hosts.jsp.')

    parser.add_argument('--connection',
                        metavar="CONNECTION",
                        required=True,
                        help='The connection name. For example, \
                                 "Demo" or "Real".')


    parser.add_argument('-session',
                        help='The database name. Required only for users who\
                                 have accounts in more than one database.\
                                 Optional parameter.')

    parser.add_argument('-pin',
                        help='Your pin code. Required only for users who have \
                                 a pin. Optional parameter.')

def add_candle_open_price_mode_argument(parser: argparse.ArgumentParser):
    parser.add_argument('--openpricemode',
                        metavar="CANDLE_OPEN_PRICE_MODE",
                        default="prev_close",
                        help='Ability to set the open price candles mode. \
                        Possible values are first_tick, prev_close. For more information see description \
                        of O2GCandleOpenPriceMode enumeration. Optional parameter.')

def add_instrument_timeframe_arguments(parser: argparse.ArgumentParser, timeframe: bool = True):
    parser.add_argument('-i','--instrument',
                        metavar="INSTRUMENT",
                        default="EUR/USD",
                        help='An instrument which you want to use in sample. \
                                  For example, "EUR/USD".')

    if timeframe:
        parser.add_argument('-t','--timeframe',
                            metavar="TIMEFRAME",
                            default="m5",
                            help='Time period which forms a single candle. \
                                      For example, m1 - for 1 minute, H1 - for 1 hour.')
    parser.add_argument('-ip',
                        metavar="IndicatorPattern",
                        required=False,
                        help='The indicator Pattern. For example, \
                                 "AOAC","JTL,"JTLAOAC","JTLAOAC","AOACMFI".')

def add_direction_rate_lots_arguments(parser: argparse.ArgumentParser, direction: bool = True, rate: bool = True,
                                      lots: bool = True):
    if direction:
        parser.add_argument('-d', metavar="TYPE", required=True,
                            help='The order direction. Possible values are: B - buy, S - sell.')
    if rate:
        parser.add_argument('-r', metavar="RATE", required=True, type=float,
                            help='Desired price of an entry order.')
    if lots:
        parser.add_argument('-lots', metavar="LOTS", default=1, type=int,
                            help='Trade amount in lots.')


def add_account_arguments(parser: argparse.ArgumentParser):
    parser.add_argument('-account', metavar="ACCOUNT",
                        help='An account which you want to use in sample.')


def str_to_datetime(date_str):
    formats = ['%m.%d.%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%Y/%m/%d', '%Y-%m-%d']
    
    for fmt in formats:
        try:
            return datetime.datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def tlid_range_to_start_end_datetime(tlid_range: str):
    start_str, end_str = tlid_range.split("_")
    
    date_format_start = "%y%m%d%H%M"
    date_format_end = "%y%m%d%H%M"
    
    if len(start_str) == 6:
        date_format_start = "%y%m%d"
    if len(end_str) == 6:
        date_format_end = "%y%m%d"
    
    #print(date_format_end)
    try:
        start_dt =  datetime.datetime.strptime(start_str, date_format_start)
        end_dt = datetime.datetime.strptime(end_str, date_format_end)
        return start_dt,end_dt
    except ValueError:
        return None

def tlid_range_to_jgtfxcon_start_end_str(tlid_range: str):
    date_format_fxcon = '%m.%d.%Y %H:%M:%S'
    start_dt,end_dt = tlid_range_to_start_end_datetime(tlid_range)
    #print(str(start_dt),str(end_dt))
    if start_dt is None or end_dt is None:
        return None,None
    else:
        return str(start_dt.strftime(date_format_fxcon)),str(end_dt.strftime(date_format_fxcon))

def tlid_dt_to_string(dt):
    return dt.strftime("%y%m%d%H%M")

def tlidmin_to_dt(tlid_str: str):
    date_format = "%y%m%d%H%M"
    try:
        tlid_dt =  datetime.datetime.strptime(tlid_str, date_format)
        return tlid_dt
    except ValueError:
        pass
    
    return None

def valid_datetime(check_future: bool):
    def _valid_datetime(str_datetime: str):
        date_format = '%m.%d.%Y %H:%M:%S'
        try:
            result = datetime.datetime.strptime(str_datetime, date_format).replace(
                tzinfo=datetime.timezone.utc)
            if check_future and result > datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc):
                msg = "'{0}' is in the future".format(str_datetime)
                raise argparse.ArgumentTypeError(msg)
            return result
        except ValueError:
            now = datetime.datetime.now()
            msg = "The date '{0}' is invalid. The valid data format is '{1}'. Example: '{2}'".format(
                str_datetime, date_format, now.strftime(date_format))
            raise argparse.ArgumentTypeError(msg)
    return _valid_datetime


def add_tlid_range_argument(parser: argparse.ArgumentParser):
    print("Tlid range active")
    parser.add_argument('-r', '--range', type=str, required=False, dest='tlidrange',
                        help='TLID range in the format YYMMDDHHMM_YYMMDDHHMM.')

def add_date_arguments(parser: argparse.ArgumentParser, date_from: bool = True, date_to: bool = True):
    if date_from:
        parser.add_argument('-s','--datefrom',
                            metavar="\"m.d.Y H:M:S\"",
                            help='Date/time from which you want to receive\
                                      historical prices. If you leave this argument as it \
                                      is, it will mean from last trading day. Format is \
                                      "m.d.Y H:M:S". Optional parameter.',
                            type=valid_datetime(True)
                            )
    if date_to:
        parser.add_argument('-e','--dateto',
                            metavar="\"m.d.Y H:M:S\"",
                            help='Datetime until which you want to receive \
                                      historical prices. If you leave this argument as it is, \
                                      it will mean to now. Format is "m.d.Y H:M:S". \
                                      Optional parameter.',
                            type=valid_datetime(False)
                            )


def add_report_date_arguments(parser: argparse.ArgumentParser, date_from: bool = True, date_to: bool = True):
    if date_from:
        parser.add_argument('-s','--datefrom',
                            metavar="\"m.d.Y H:M:S\"",
                            help='Datetime from which you want to receive\
                                      combo account statement report. If you leave this argument as it \
                                      is, it will mean from last month. Format is \
                                      "m.d.Y H:M:S". Optional parameter.',
                            type=valid_datetime(True)
                            )
    if date_to:
        parser.add_argument('-e','--dateto',
                            metavar="\"m.d.Y H:M:S\"",
                            help='Datetime until which you want to receive \
                                      combo account statement report. If you leave this argument as it is, \
                                      it will mean to now. Format is "m.d.Y H:M:S". \
                                      Optional parameter.',
                            type=valid_datetime(True)
                            )


def add_max_bars_arguments(parser: argparse.ArgumentParser):
    parser.add_argument('-c','--quotescount',
                        metavar="MAX",
                        default=335,
                        type=int,
                        help='Max number of bars. 0 - Not limited')


# def add_bars_arguments(parser: argparse.ArgumentParser):
#     parser.add_argument('-bars',
#                         metavar="COUNT",
#                         default=3,
#                         type=int,
#                         help='Build COUNT bars. Optional parameter.')


def add_output_argument(parser: argparse.ArgumentParser):
    """
    Adds an output argument to the given argument parser.

    Args:
        parser (argparse.ArgumentParser): The argument parser to add the output argument to.

    Returns:
        None
    """
    parser.add_argument('-o','--output',
                        action='store_true',
                        help='Output file. If specified, output will be written in the filestore.')
    
    parser.add_argument('-z','--compress',
                        action='store_true',
                        help='Compress the output. If specified, it will also activate the output flag.')

    return parser


# def add_quiet_argument(parser):
#     parser.add_argument('-q','--quiet',
#                         action='store_true',
#                         help='Suppress all output. If specified, no output will be printed to the console.')
#     return parser

def add_verbose_argument(parser):
    parser.add_argument('-v', '--verbose',
                        type=int,
                        default=0,
                        help='Set the verbosity level. 0 = quiet, 1 = normal, 2 = verbose, 3 = very verbose, etc.')
    return parser

def add_cds_argument(parser):
    parser.add_argument('-cds','--cds',
                        action='store_true',
                        default=False,
                        help='Action the creation of CDS')
    return parser

def add_iprop_init_argument(parser):
    parser.add_argument('-iprop','--iprop',
                        action='store_true',
                        default=False,
                        help='Toggle the downloads of all instrument properties ')
    return parser

def add_debug_argument(parser):
    parser.add_argument('-debug','--debug',
                        action='store_true',
                        default=False,
                        help='Toggle debug ')
    return parser

def add_pdsserver_argument(parser):
    parser.add_argument('-server','--server',
                        action='store_true',
                        default=False,
                        help='Run the server ')
    return parser


def print_exception(exception: Exception):
    logging.error("Exception: {0}\n{1}".format(exception, traceback.format_exc()))











def diff_month(year: int, month: int, date2: datetime):
    return (year - date2.year) * 12 + month - date2.month






_JGT_CONFIG_JSON_SECRET=None

def readconfig(json_config_str=None):
    global _JGT_CONFIG_JSON_SECRET
    # Try reading config file from current directory

    if json_config_str is not None:
        config = json.loads(json_config_str)
        _JGT_CONFIG_JSON_SECRET=json_config_str
        return config


    if _JGT_CONFIG_JSON_SECRET is not None:
        config = json.loads(_JGT_CONFIG_JSON_SECRET)
        return config
    
    # Otherwise, try reading config file from current directory, home or env var
    config_file = 'config.json'
    config = None

    if os.path.isfile(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config
    else:
        # If config file not found, check home directory
        home_dir = os.path.expanduser("~")
        config_file = os.path.join(home_dir, 'config.json')
        if os.path.isfile(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
        else:
            # If config file still not found, try reading from environment variable
            config_json_str = os.getenv('JGT_CONFIG_JSON_SECRET')
            if config_json_str:
                config = json.loads(config_json_str)
                return config


    # Now you can use the config dictionary in your application

    # Read config file
    with open(config_file, 'r') as file:
        config = json.load(file)
        
    if config is None:
        raise Exception("Configuration not found")
    
    return config
