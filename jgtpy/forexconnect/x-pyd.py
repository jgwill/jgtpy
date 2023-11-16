
import sys
import os
import sys


here = os.path.abspath(os.path.dirname(__file__))
print(here)
lib_path=os.path.join(here,'lib','windows')
print(lib_path)
# Add the directory containing fxcorepy.pyd to the Python path
sys.path.append(lib_path)

# Add the directory containing the DLLs to the PATH
os.environ['PATH'] += os.pathsep + lib_path


# Now try to import the module
#import fxcorepy
from lib.windows import fxcorepy as fxcorepy