import os
import platform
import sys

origin_work_dir = os.getcwd()
here = os.path.abspath(os.path.dirname(__file__))

os.chdir(here)

lib_path = os.path.join(here, "lib")

if platform.system() == 'Windows':
    print("----------------Windows------------")
    lib_path = os.path.join(here, 'lib', 'windows')
    os.chdir(lib_path)
    #os.add_dll_directory(lib_path)
    # sys.path.append(lib_path)
    # os.environ['PATH'] += os.pathsep + lib_path  # Add lib_path to PATH
    #from .lib.windows import ForexConnect as fxfuck
    #print(lib_path)
    try:
    #      #import forexconnect
        from .lib.windows import fxcorepy 
    except:
        pass
        #from . import fxcorepy
         
    # from .lib.windows import *
elif platform.system() == 'Linux':
    #print("----------------Linux------------")
    lib_path = os.path.join(here, 'lib', 'linux')
    os.chdir(lib_path)
    try:
         #import forexconnect
         from .lib.linux import fxcorepy as fxcorepy
    except:
        try:
            print("-----------EXCEPTION --- #import forexconnect")
            print("---from .lib.linux import fxcorepy as fxcorepy---")
            #import jgtpy.forexconnect as forexconnect
            from jgtpy.forexconnect.lib.linux import fxcorepy as fxcorepy
        except:
            from . import fxcorepy
        
else:
    raise RuntimeError('Unsupported platform')

#print(lib_path)
os.chdir(here)
os.chdir(origin_work_dir)

#from .lib import fxcorepy
from .ForexConnect import ForexConnect
from .TableManagerListener import TableManagerListener
from .SessionStatusListener import SessionStatusListener
from .LiveHistory import LiveHistoryCreator
from .EachRowListener import EachRowListener
from .ResponseListener import ResponseListener, ResponseListenerAsync
from .TableListener import TableListener
from .common import Common

fxcorepy.O2GTransport.set_transport_modules_path(lib_path)

os.chdir(origin_work_dir)   
