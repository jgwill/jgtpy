import os
import sys
#sys.path.insert(0, os.path.abspath('../'))
#sys.path.insert(0, os.path.abspath('../jgtpy'))
from jgtpy import __version__
import jgtpy
from jgtpy import JGTPDSP,JGTIDS,JGTCDS,jgtetl,JGTCDSSvc,JGTPDSRequest,JGTIDSRequest,JGTCDSRequest,JGTMKSG,JGTADS,jgtapyhelper

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

