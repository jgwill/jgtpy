# Copyright 2024 Jean Guillaume Isabelle
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


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))



import warnings

with warnings.catch_warnings():
    warnings.filterwarnings(
        "ignore", category=RuntimeWarning, module="importlib._bootstrap"
    )



from JGTCore import (
    __version__,
) 


from JGTCDS import (
    create as cds_create,
    createFromDF as fromdf,
    readCDSFile as read,
)

import JGTADS as ads
from JGTADS import plot as plot,plot as ads_create

import JGTMKSG as mksg
from JGTMKSG import (
    pto_generate_snapshot_240302_v2_by_crop_dates as mksg_by_crop_dates,
    pto_generate_snapshot_240302_v2_by_crop_dates as mksg_create_crops,
    generate_market_snapshots as mksg_by_pov,
    generate_market_snapshots as mksg_create_pov,
)


def help():
    print(
        "JGTPY\n",
        "Version: ",
        __version__,
        "\n",
        "JGTPY is a set of tools to help with the analysis of financial markets.\n",
        "It is a Python library that can be used to process data from various sources.\n",
        "It is also a command line tool that can be used to generate charts and reports.\n",
        "> import jgtpy as jgt\n",
        "> i=\"SPX500\"\n",
        "> t=\"H4\"\n",
        "> #CDS \n",
        "> df=jgt.cds_create(i,t)\n",
        "> df_fresh=jgt.cds_create(i,t,use_fresh=True)\n",
        "> df_fresh_full=jgt.cds_create(i,t,use_fresh=True,use_full=True)\n",
        "> \n",
        "> \n",
        "> #ADS \n",
        "> ads_chart,_ads_plt_arr,_ads_df = jgt.ads(i,t)\n",
        "> ads_chart.show()\n",
        "> \n",
        "> df=jgt.read(i,t)\n",
        "> \n",
        "> #MKS \n",
        "> jgt.mksg_by_crop_dates(i,t,\"H4\",\"Fractal\",\"2023-01-01\",scn_root_dir=\"./data\",show_chart=True,show_tabs=True,save_fig_image=True,save_cds_data=True)\n",
        "> \n",
        "For more information, please visit: https://jgtpy.jgwill.com\n"        
    )
