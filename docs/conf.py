import os
import sys
sys.path.insert(0, os.path.abspath('../'))
from jgtpy import __version__
autodoc_mock_imports = ['pandas']

project = 'jgtpy'
copyright = '2022, Guillaume Isabellle'
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

intersphinx_mapping = {'http://docs.python.org/': None}