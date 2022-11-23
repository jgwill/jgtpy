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
from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout
            
import argparse
import importlib

import pandas as pd
import datetime
import tzdata
#from forexconnect import ForexConnect, fxcorepy

import JGTPDS as pds

import jgtcommon


traded_lots = 3
nb2retrieve=335

def parse_args():
    parser = argparse.ArgumentParser(description='Process command parameters.')
    #common_samples.add_main_arguments(parser)
    jgtcommon.add_instrument_timeframe_arguments(parser)
    #common_samples.add_date_arguments(parser)
    jgtcommon.add_nb2retrieve_arguments(parser)
    jgtcommon.add_out_pov(parser)
    jgtcommon.add_local_arguments(parser)
    # common_samples.add_max_bars_arguments(parser)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    # str_user_id = args.l
    # str_password = args.p
    # str_url = args.u
    # str_connection = args.c
    # str_session_id = args.session
    # str_pin = args.pin
    str_instrument = args.i
    str_timeframe = args.timeframe
    nb = args.nb
    str_outfile = jgtcommon.get_opov_filenamed(args)
    local_read=args.local
    pds.useLocal=local_read
    # tf=str_timeframe
    # if tf=="m1":
    #     tf="mi1"
    # str_opov = args.opov
    # filesufext ="."+ str_opov + ".csv"
   
    # quotes_count = args.quotescount
    # date_from = args.datefrom
    # date_to = args.dateto
    df=pd.DataFrame()
    with suppress_stdout():
        df=pds.getPH(str_instrument,str_timeframe,nb)
    print(df) 
    df.to_csv(str_outfile)
    print("Created: "+str_outfile) 
    pds.disconnect()
    # except Exception as e:
    #     common_samples.print_exception(e)
    # try:
    #     fx.logout()
    # except Exception as e:
    #     common_samples.print_exception(e)


if __name__ == "__main__":
    main()
    print("DONE")
    #input("Done! Press enter key to exit\n")
