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


import os
import platform
import sys

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


import jgtflags


import warnings

with warnings.catch_warnings():
    warnings.filterwarnings(
        "ignore", category=RuntimeWarning, module="importlib._bootstrap"
    )
    # your code here


class NotCompatibleException(Exception):
    pass


# from jgtpy.common_samples import common_samples
from jgtetl import svc_offset_dt_by_tf as etl_offset_dt_by_tf, offsetdt as etl_offsetdt
from JGTCore import (
    __version__,
)  # ,json2dict,jsonfile2prop,json2prop,jsonfile2dict,d2p,fixdtindf,offsetdt

# from .JGTConfig import getenv,setreal,setdemo,env


from jgtutils import jgtwslhelper as wsl

import JGTIDS as ids, JGTADS as ads, JGTPDSP as pds, JGTCDS as cds

from JGTIDS import tocds as tocds

# mk_fn,mk_fullpath,getSubscribed,getPH,getPHByRange,tryConnect
from JGTCDS import (
    create as createCDS,
    createByRange,
    createFromDF,
    getLast,
    getPresentBar,
    getPresentBarAsList,
    getLastCompletedBarAsList,
    createFromDF,
    createFromFile_and_clean_and_save_data as fromfile,
    createFromFile_and_clean_and_save_data as ff,
    createFromDF as fp,
    readCDSFile as rcds,
)
from JGTADS import plot as plot
import jgtpy.JGTMKSG as mksg


def help():
    print(
        ".h(i,t,400)\t\tGet Prices (PDS): \n\t\t\tjgtpy.h(instrument,timeframe,quote_count=335,start=None,end=None,quiet=True)"
    )
    print("\t\t\t\t\treturn DataFrame of PDS Type")
    print("\t\t\t\t\t(Will connect and stay connected)")
    print(".fp(df)\t\t Create CDS from PDS DF \n\t\t\tjgtpy.fp(df [pd.DataFrame])")
    print("\t\t\t\t\treturn DataFrame of CDS Type")
    print(".off()\t\t Disconnect (Bugged)\n\t\t\tjgtpy.off()")
