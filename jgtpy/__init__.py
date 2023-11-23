# Copyright 2023 Jean Guillaume Isabelle
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Jean Guillaume Isabelle <jgi@jgwill.com>
"""

# from jgtfxcommon.BatchOrderMonitor import BatchOrderMonitor
# from jgtfxcommon.OrderMonitor import OrderMonitor
# from jgtfxcommon.OrderMonitorNetting import OrderMonitorNetting
# from jgtfxcommon.TableListenerContainer import TableListenerContainer
# from jgtfxcommon.common import add_main_arguments, add_instrument_timeframe_arguments, \
#     add_candle_open_price_mode_argument, add_direction_rate_lots_arguments, add_account_arguments, \
#     valid_datetime, add_date_arguments, add_report_date_arguments, add_max_bars_arguments, add_bars_arguments, \
#     print_exception, session_status_changed, diff_month, convert_timeframe_to_seconds

import os
import platform
import sys
from . import jgtflags

class NotCompatibleException(Exception):
    pass

#from jgtpy.common_samples import common_samples
from .jgtetl import svc_offset_dt_by_tf as etl_offset_dt_by_tf,offsetdt as etl_offsetdt
from .JGTCore import __version__ #,json2dict,jsonfile2prop,json2prop,jsonfile2dict,d2p,fixdtindf,offsetdt
#from .JGTConfig import getenv,setreal,setdemo,env

if platform.system() == 'Linux':
  #sys.path.append(os.path.abspath('./'))

  origin_work_dir = os.getcwd()
  here = os.path.abspath(os.path.dirname(__file__))
  os.chdir(here)
  try:
     from . import forexconnect
  except:
     from jgtpy import forexconnect 
  os.chdir(origin_work_dir)   

else:
  try:
    try:
      from . import forexconnect       
    except:
     from jgtpy import forexconnect 
  except:
    print("----------------------------------------------------------------")
    print("---Failed to load forexconnect --- Please Install forexconnect")
    print("--------- > pip install forexconnect (only an python =< 3.7)")
    print("--------")
    print("-----WINDOWS USER : ----")
    print("--If you are on an above Windows Python 3.7, it wont work.  ")
    print("--I made forexconnect to work on later than 3.7 only on Linux, ")
    print("-- sorry guys, migrate on Linux ;) or get involved migrating it ;) ")
    print("-----------------------------------------")
    raise NotCompatibleException("Forexconnect is not compatible with your current environment.")



# os.chdir(origin_work_dir)   
from .jgtfxcommon import _JGT_CONFIG_JSON_SECRET


from .JGTPDS import getPH as get_price, stayConnectedSetter as set_stay_connected, disconnect,connect as on,disconnect as off, status as connection_status,  getPH2file as get_price_to_file, getPHByRange as get_price_range, stayConnectedSetter as sc,getPH as ph
def stay():
    sc(True)
def up():
    sc(False)
def h(instrument,timeframe,quote_count=335,start=None,end=None,quiet=True):
        stay()
        return ph(instrument,timeframe,quote_count,start,end,False,quiet)

from .JGTIDS import tocds as tocds
#mk_fn,mk_fullpath,getSubscribed,getPH,getPHByRange,tryConnect
from .JGTCDS import create as createCDS,createByRange,createFromDF,startSession,stopSession,getLast,getPresentBar,getPresentBarAsList,getLastCompletedBarAsList,createFromDF,createFromFile_and_clean_and_save_data as fromfile,createFromFile_and_clean_and_save_data as ff,createFromDF as fp

def help():
    print(".h(i,t,400)\t\tGet Prices (PDS): \n\t\t\tjgtpy.h(instrument,timeframe,quote_count=335,start=None,end=None,quiet=True)")
    print("\t\t\t\t\treturn DataFrame of PDS Type")
    print("\t\t\t\t\t(Will connect and stay connected)")
    print(".fp(df)\t\t Create CDS from PDS DF \n\t\t\tjgtpy.fp(df [pd.DataFrame])")
    print("\t\t\t\t\treturn DataFrame of CDS Type")
    print(".off()\t\t Disconnect (Bugged)\n\t\t\tjgtpy.off()")

# from jgtpy.JGTADS import ads_chart_pto,retrieve_n_chart as ads_retrieve_n_chart

# from .jgtcli import main as __main__
#from jgtpy.jgtconstants import *

