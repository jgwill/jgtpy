# Purpose of JGTIDS.py

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

For more details, you can refer to the implementation in `jgtpy/JGTIDS.py`, `jgtpy/JGTCDS.py`, and `jgtpy/JGTCDSSvc.py`. The columns are also wrapped in `jgtpy/jgtcli.py`.
