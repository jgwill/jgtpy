
import sys
import os
import pandas as pd
import json


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
  
from JGTIDS import _ids_add_fdb_column_logics_v2

from JGTIDSRequest import JGTIDSRequest

from jgtapyhelper import createIDSService
import jgtapyhelper as th

#@STCGoal Wrap the JGTIDS and jgtapyhelper classes into a service class


def get_ids(rq:JGTIDSRequest):
    try:
      idspath, idf=createIDSService(
                    rq=rq,
                    quiet=rq.quiet,
                    verbose_level=rq.verbose_level,
                )
      idf=_ids_add_fdb_column_logics_v2(idf)
      return idf
        
    except:
      print("IDS failed")
      return None
    
  