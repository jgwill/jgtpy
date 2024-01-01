.. jgtapy documentation master file, created by
   sphinx-quickstart on Mon Sep 23 02:03:02 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to jgtpy's documentation!
================================

:Source Code: https://github.com/jgwill/jgtpy
:Issue Tracker: https://github.com/jgwill/jgtpy/issues
:PyPi: https://pypi.org/project/jgtpy/

.. automodule:: jgtpy
   :members: __doc__

.. toctree::
   :maxdepth: 3
   :caption: Contents

   index

Installation
============
::

   pip install jgtpy

Indicators
==========
.. autoclass:: jgtpy.JGTPDS
.. autoclass:: jgtpy.JGTIDS
.. autoclass:: jgtpy.JGTCDS
.. autoclass:: jgtpy.JGTADS
.. automodule:: __init__
.. automodule:: jgtpy.JGTPDS
.. automodule:: jgtpy.JGTIDS
.. automodule:: jgtpy.JGTCDS
.. automodule:: jgtpy.JGTADS




========== 

.. req:: A normal requirement
   :id: EX_REQ_1
   :status: open

   This is how a normal requirement looks like

.. req:: A more complex and highlighted requirement
   :id: EX_REQ_2
   :status: open
   :tags: awesome, nice, great
   :links: EX_REQ_1
   :layout: complete
   :style: red_border

   More columns for better data structure and a red border.

.. req:: A focused requirement
   :id: EX_REQ_3
   :status: open
   :style: red
   :layout: focus_r

   This also a requirement, but we focus on content here.
   All meta-data is hidden.

.. req:: A custom requirement with picture
   :author: daniel
   :id: EX_REQ_4
   :tags: example
   :status: open
   :layout: example
   :style: yellow, blue_border

   This example uses the value from **author** to reference an image.
   See :ref:`layouts_styles` for the complete explanation.

.. req:: A requirement with a permalink
   :id: EX_REQ_5
   :tags: example
   :status: open
   :layout: permalink_example

   
