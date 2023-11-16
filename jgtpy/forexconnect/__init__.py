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
    # sys.path.append(lib_path)
    # os.environ['PATH'] += os.pathsep + lib_path  # Add lib_path to PATH
    #from forexconnect.lib.windows import ForexConnect as fxfuck
    print(lib_path)
    from .lib.windows import *
elif platform.system() == 'Linux':
    print("----------------Linux------------")
    lib_path = os.path.join(here, 'lib', 'linux')
    os.chdir(lib_path)
    try:
         import forexconnect
         from forexconnect.lib.linux import fxcorepy as fxcorepy
    except:
        import jgtpy.forexconnect as forexconnect
        from jgtpy.forexconnect.lib.linux import fxcorepy as fxcorepy
        
else:
    raise RuntimeError('Unsupported platform')

#print(lib_path)
os.chdir(here)
#from forexconnect.lib import fxcorepy
from forexconnect.ForexConnect import ForexConnect
from forexconnect.TableManagerListener import TableManagerListener
from forexconnect.SessionStatusListener import SessionStatusListener
from forexconnect.LiveHistory import LiveHistoryCreator
from forexconnect.EachRowListener import EachRowListener
from forexconnect.ResponseListener import ResponseListener, ResponseListenerAsync
from forexconnect.TableListener import TableListener
from forexconnect.common import Common

fxcorepy.O2GTransport.set_transport_modules_path(lib_path)

os.chdir(origin_work_dir)   