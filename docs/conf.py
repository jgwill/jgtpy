import os
import sys
sys.path.insert(0, os.path.abspath('../'))
#sys.path.insert(0, os.path.abspath('../jgtpy'))
from jgtpy import __version__
#import ..jgtpy



def setup(app):
    # Import the module directly
    from jgtpy import JGTPDSP,JGTIDS,JGTCDS,JGTCDSSvc,JGTPDSRequest,JGTIDSRequest,JGTCDSRequest,JGTMKSG,JGTADS,jgtapyhelper
    #from jgtpy import JGTCDSSvc

    # Adjust the __module__ attribute of the module or its classes
    # If you want to adjust it for specific classes within the module, do it here
    JGTCDSSvc.__module__ = "jgtpy.JGTCDSSvc"
    JGTADS.__module__ = "jgtpy.JGTADS"
    JGTMKSG.__module__ = "jgtpy.JGTMKSG"
    JGTCDS.__module__ = "jgtpy.JGTCDS"
    JGTIDS.__module__ = "jgtpy.JGTIDS"
    JGTPDSP.__module__ = "jgtpy.JGTPDSP"
    jgtapyhelper.__module__ = "jgtpy.jgtapyhelper"
    JGTIDSRequest.__module__ = "jgtpy.JGTIDSRequest"
    JGTCDSSvc.__module__ = "jgtpy.JGTCDSSvc"
    JGTPDSRequest.__module__ = "jgtpy.JGTPDSRequest"
    JGTCDSRequest.__module__ = "jgtpy.JGTCDSRequest"
    

    # If JGTCDSSvc is a module containing classes you wish to document, iterate over them
    for attr_name in dir(JGTCDSSvc):
        attr = getattr(JGTCDSSvc, attr_name)
        if isinstance(attr, type):  # Check if it's a class
            attr.__module__ = "jgtpy.JGTCDSSvc"
    for attr_name in dir(JGTADS):
        attr = getattr(JGTADS, attr_name)
        if isinstance(attr, type):
            attr.__module__ = "jgtpy.JGTADS"
    for attr_name in dir(JGTMKSG):
        attr = getattr(JGTMKSG, attr_name)
        if isinstance(attr, type):
            attr.__module__ = "jgtpy.JGTMKSG"
    for attr_name in dir(JGTCDS):
        attr = getattr(JGTCDS, attr_name)
        if isinstance(attr, type):
            attr.__module__ = "jgtpy.JGTCDS"
    


autodoc_mock_imports = ['pandas']

project = 'jgtpy'
copyright = '2024, Guillaume Isabelle'
author = 'Guillaume Isabelle'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']

source_suffix = '.rst'
master_doc = 'index'

version = __version__
release = __version__

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Comment out or remove this line if the _static directory doesn't exist
# html_static_path = ['_static']

pygments_style = 'default'

html_theme = 'sphinx_rtd_theme'
# Make sure to update sphinx_rtd_theme to the latest version

htmlhelp_basename = 'JGTPyDoc'

latex_documents = [
  ('index', 'TaPy.tex', 'JGTPy Documentation',
   'JGTPy Contributors', 'manual'),
]

# Updated format
#intersphinx_mapping = {'python': ('http://docs.python.org/', None)}
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable', None),
    #'jgtapy': ('https://jgtapy.jgwill.com', None)
}

