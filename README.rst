jgtpy
====

Enhanced JGTPy CDS, IDS, PDS Services


* Please see the README.md  - that file is outdated.

Installation
------------

::

    pip install -U jgtpy

Example
-------

::


    >>> import pandas as pd
    >>> import jgtpy 
    >>> df=jgtpy.getPH('EUR/USD','H4')
    >>>
    >>> # retrieve 3000 periods and generate from the DF
    >>> df=jgtpy.getPH('EUR/USD','H4',3000,with_index=False)
    >>> dfi=jgtpy.createFromDF(df)
    >>>
    >>> # Create with Timerange
    >>> start="11.17.2022 00:00:00"
    >>> end="11.25.2022 00:00:00"
    >>> df=jgtpy.createByRange("USD/CAD","m15",start,end)
    >>>
    >>> # offsets date for retreival
    >>> dtfirst_with_offset=jgtetl.svc_offset_dt_by_tf(dtfirst,ctx.timeframe)
    >>> df=createByRange(ctx.instrument,ctx.timeframe,dtfirst_with_offset,dtlast)


APPENDIX
--------

### IDS Data Columns

The `jgtpy/JGTIDS.py` file is responsible for generating and managing IDS (Indicator Data Service) files. Here is a Markdown table documenting all the columns in `JGTIDS.py` that are in the output:

| Column Name | Description |
|-------------|-------------|
| `Date` | The date and time of the data point. |
| `Open` | The opening price of the data point. |
| `High` | The highest price of the data point. |
| `Low` | The lowest price of the data point. |
| `Close` | The closing price of the data point. |
| `Volume` | The volume of the data point. |
| `Median` | The median price of the data point. |
| `ao` | The Awesome Oscillator value. |
| `ac` | The Acceleration/Deceleration Oscillator value. |
| `jaw` | The Alligator's jaw value. |
| `teeth` | The Alligator's teeth value. |
| `lips` | The Alligator's lips value. |
| `fh` | The fractal high value. |
| `fl` | The fractal low value. |
| `fdb` | The fractal divergent bar value. |
| `fdbb` | The fractal divergent bar buy signal. |
| `fdbs` | The fractal divergent bar sell signal. |
| `zlc` | The zero line cross value. |
| `zlcB` | The zero line cross buy signal. |
| `zlcS` | The zero line cross sell signal. |
| `bz` | The buy zone signal. |
| `sz` | The sell zone signal. |
| `aocolor` | The color of the Awesome Oscillator. |
| `accolor` | The color of the Acceleration/Deceleration Oscillator. |
| `aof` | The AO fractal peak value. |
| `aofvalue` | The AO fractal peak value. |
| `aofhighao` | The AO value on the bullish peak. |
| `aoflowao` | The AO value on the bearish peak. |
| `aofhigh` | The price high of the peak. |
| `aoflow` | The price low of the peak. |
| `mfi` | The Market Facilitation Index value. |
| `mfi_squat` | The MFI squat signal. |
| `mfi_green` | The MFI green signal. |
| `mfi_fade` | The MFI fade signal. |
| `mfi_fake` | The MFI fake signal. |
| `mfi_signal` | The MFI signal value. |
| `mfi_val` | The MFI value. |
| `zone_signal` | The zone signal value. |
| `zone_int` | The zone integer value. |

### CDS Data Columns

The `jgtpy/JGTCDS.py` file is responsible for creating, reading, and managing Chaos Data Service (CDS) files from Price Data Service (PDS) files. Here is a Markdown table documenting all the columns in `JGTCDS.py` that are added after using `JGTIDS.py` and are in the output:

| Column Name | Description |
|-------------|-------------|
| `fdbbhigh` | The high value of the fractal divergent bar buy signal. |
| `fdbblow` | The low value of the fractal divergent bar buy signal. |
| `fdbshigh` | The high value of the fractal divergent bar sell signal. |
| `fdbslow` | The low value of the fractal divergent bar sell signal. |
| `aocolor` | The color of the Awesome Oscillator. |
| `accolor` | The color of the Acceleration/Deceleration Oscillator. |
| `zcol` | The zone color value. |
| `zlc` | The zero line cross value. |
| `zlcB` | The zero line cross buy signal. |
| `zlcS` | The zero line cross sell signal. |
| `bz` | The buy zone signal. |
| `sz` | The sell zone signal. |
| `mfi_squat` | The MFI squat signal. |
| `mfi_green` | The MFI green signal. |
| `mfi_fade` | The MFI fade signal. |
| `mfi_fake` | The MFI fake signal. |
| `mfi_signal` | The MFI signal value. |
| `mfi_val` | The MFI value. |
| `zone_signal` | The zone signal value. |
| `zone_int` | The zone integer value. |

### IDS Purpose

The `jgtpy/JGTIDS.py` file is responsible for generating and managing IDS (Indicator Data Service) files. The `jgtids` script, exposed through `[project.scripts]` in `pyproject.toml`, provides functionalities to create IDS files, read IDS files, and perform other related operations. Here is a detailed documentation of the purpose of JGTIDS and what end-results it produces in terms of data for `JGTCDS.py`:

* **Purpose of JGTIDS** 📊
  - The main purpose of `JGTIDS.py` is to add various technical indicators to the financial market data. These indicators are used for market analysis and trading decisions.
  - The module processes the input data and adds indicators such as the Alligator indicator, Awesome Oscillator (AO), Acceleration/Deceleration Oscillator (AC), fractals, and Market Facilitation Index (MFI).
  - The module also generates buy and sell signals based on the technical indicators. These signals include fractal divergent bar signals, zero line cross signals, and zone signals.

* **End-Results Produced for JGTCDS.py** 📈
  - The processed data with added indicators and signals is used as input for `JGTCDS.py` to create Chaos Data Service (CDS) files.
  - The indicators and signals added by `JGTIDS.py` are essential for generating the CDS files, which are used for further analysis and charting.
  - The columns added by `JGTIDS.py` include various technical indicators and signals, which are documented in the `docs/IDS_data_columns.md` file.

* **Data Flow** 🔄
  - The input data is read from Price Data Service (PDS) files.
  - The data is processed by `JGTIDS.py` to add indicators and signals.
  - The processed data is then used by `JGTCDS.py` to create CDS files.
  - The CDS files are used for further analysis, charting, and generating trading signals.

### CDS Purpose

The `jgtpy/JGTCDS.py` file is responsible for creating, reading, and managing Chaos Data Service (CDS) files from Price Data Service (PDS) files. Here is a detailed documentation of the purpose of JGTCDS and what it produces after getting data from `JGTIDS.py`:

* **Purpose of JGTCDS** 📊
  - The main purpose of `JGTCDS.py` is to process the input data from `JGTIDS.py` and create CDS files. These files contain processed financial market data with various technical indicators and signals.
  - The module provides functions to create CDS files from PDS files, read CDS files, and manage the data. It also handles data cleansing and normalization.

* **Data Processing** 🔄
  - The input data is read from PDS files and processed by `JGTIDS.py` to add various technical indicators and signals.
  - The processed data from `JGTIDS.py` is then used by `JGTCDS.py` to create CDS files. The module adds additional indicators and signals to the data, such as fractal divergent bar signals, zero line cross signals, and zone signals.
  - The data is cleansed and normalized to ensure it is ready for analysis and charting.

* **End-Results Produced** 📈
  - The CDS files created by `JGTCDS.py` contain processed financial market data with various technical indicators and signals. These files are used for further analysis, charting, and generating trading signals.
  - The columns added by `JGTCDS.py` include various technical indicators and signals, which are documented in the `docs/CDS_data_columns.md` file.

* **Data Flow** 🔄
  - The input data is read from Price Data Service (PDS) files.
  - The data is processed by `JGTIDS.py` to add indicators and signals.
  - The processed data is then used by `JGTCDS.py` to create CDS files.
  - The CDS files are used for further analysis, charting, and generating trading signals.

### CDSSvc Purpose

The `jgtpy/JGTCDSSvc.py` file is responsible for providing services related to Chaos Data Service (CDS) files. Here is a detailed documentation of the purpose of JGTCDSSvc and what it produces:

* **Purpose of JGTCDSSvc** 📊
  - The main purpose of `JGTCDSSvc.py` is to provide functionalities for creating, reading, and managing CDS files. It acts as a service layer that interacts with `JGTCDS.py` to perform these operations.
  - The module provides functions to create CDS files from PDS files, read CDS files, and manage the data. It also handles data cleansing and normalization.

* **Data Processing** 🔄
  - The input data is read from PDS files and processed by `JGTIDS.py` to add various technical indicators and signals.
  - The processed data from `JGTIDS.py` is then used by `JGTCDS.py` to create CDS files. The module adds additional indicators and signals to the data, such as fractal divergent bar signals, zero line cross signals, and zone signals.
  - The data is cleansed and normalized to ensure it is ready for analysis and charting.

* **End-Results Produced** 📈
  - The CDS files created by `JGTCDSSvc.py` contain processed financial market data with various technical indicators and signals. These files are used for further analysis, charting, and generating trading signals.
  - The columns added by `JGTCDSSvc.py` include various technical indicators and signals, which are documented in the `docs/CDS_data_columns.md` file.

* **Data Flow** 🔄
  - The input data is read from Price Data Service (PDS) files.
  - The data is processed by `JGTIDS.py` to add indicators and signals.
  - The processed data is then used by `JGTCDS.py` to create CDS files.
  - The CDS files are used for further analysis, charting, and generating trading signals.

* **Functions Not Covered in JGTCDS.py** 📜
  - **zone_update**: This function updates the zone data for a given instrument and timeframe. It reads the CDS file, extracts the zone information, and saves it to a separate file.
  - **zone_update_from_cdf**: This function updates the zone data from a given CDS DataFrame. It extracts the zone information and saves it to a separate file.
  - **zone_read**: This function reads the zone data for a given instrument and timeframe from the saved file.
  - **zone_read_up**: This function reads the zone data for a given instrument and timeframe, including higher timeframes up to a specified level.
  - **get_higher_cdf_datasets**: This function retrieves the CDS data for higher timeframes of a given instrument and timeframe. It uses parallel processing to speed up the retrieval.
  - **get_higher_cdf_datasets_no_concurrence**: This function retrieves the CDS data for higher timeframes of a given instrument and timeframe without using parallel processing.
  - **get_higher_cdf**: This function retrieves the CDS data for a higher timeframe of a given instrument and timeframe based on a specified level.

Command Line Tools
------------------

The package provides the following command-line tools for working with IDS, CDS, and related data services:

+--------------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------+
| Command      | Entry Point                   | Description                                                                                                                              |
+==============+===============================+==========================================================================================================================================+
| jgtcli       | jgtpy.jgtcli:main             | General CLI for instrument/timeframe data operations: fetch, process, and chart PDS/IDS/CDS/ADS data. Handles argument parsing for      |
|              |                               | instruments, timeframes, date ranges, and indicator options.                                                                             |
+--------------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------+
| cdscli       | jgtpy.cdscli:main             | CLI for creating and processing Chaos Data Service (CDS) files from instrument/timeframe data, with support for indicator and ADS options.|
+--------------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------+
| pds2cds      | jgtpy.pds2cds:main            | Convert a PDS (Price Data Service) file to a CDS (Chaos Data Service) file, with options for bar count and TLID date range.             |
+--------------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------+
| jgtmksg      | jgtpy.JGTMKSG:main            | Generate market snapshots and chart visualizations for multiple instruments/timeframes, with advanced charting and HTML output options.  |
+--------------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------+
| jgtads       | jgtpy.JGTADS:main             | Generate and plot Advanced Data Service (ADS) analytics and visualizations from CDS or PDS data, including technical indicators and signals.|
+--------------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------+
| jgtids       | jgtpy.jgtapycli:main          | Generate and process Indicator Data Service (IDS) files, with CLI options for indicators, normalization, and output.                    |
+--------------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------+
| adscli       | jgtpy.JGTADS:main             | Alias for `jgtads`: generate and plot ADS analytics and visualizations.                                                                 |
+--------------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------+
| mkscli       | jgtpy.JGTMKSG:main            | Alias for `jgtmksg`: generate market snapshots and chart visualizations.                                                                |
+--------------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------+
| idscli       | jgtpy.jgtapycli:main          | Alias for `jgtids`: generate and process IDS files.                                                                                     |
+--------------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------+
| adsfromcds   | jgtpy.adsfromcdsfile:main     | Create plots from CDS cache data, supporting custom output directories, chart types, and feature plots.                                 |
+--------------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------+

For more information on each command, see the documentation in the ``docs/`` directory or run each command with ``--help``.

