# JGT PDS
#
# Copyright 20.1.4022 Jean Guillaume Isabelle
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

# # import fxcmpy
# # import datetime as dt
# # import pandas as pd
# #import fxcmpy and check the imported version
import fxcmpy as fx
# import datetime as dt
# import pandas as pd
# #fxcmpy.__version__
# import jgtpy.JGTConfig as jgtc


# import jgtpy.JGTPDHelper as jpd
# import jgtpy.JGTPDHelper
# import jgtpy.JGTFXCMWrapper as jfx
# import jgtpy.JGTConfig as jgtcnf
# import jgtpy.JGTPDS as pds
# import jgtpy.JGTCDS as cds
# import jgtpy.JGTIDS as ids
from jgtpy.JGTCore import __version__

from jgtpy.JGTPDS import mk_fn,mk_fullpath,getSubscribed,getPH,getPHByRange,tryConnect
from jgtpy.JGTCDS import create as createCDS,startSession,stopSession,getLast,getPresentBar,getPresentBarAsList,getLastCompletedBarAsList
# from jgtpy.JGTADS import ads_chart_pto,retrieve_n_chart as ads_retrieve_n_chart

