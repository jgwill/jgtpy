# Purpose of JGTCDSSvc.py

The `jgtpy/JGTCDSSvc.py` file is responsible for providing services related to Chaos Data Service (CDS) files. Here is a detailed documentation of the purpose of JGTCDSSvc and what it produces:

* **Purpose of JGTCDSSvc** 📊
  - The main purpose of `JGTCDSSvc.py` is to provide functionalities for creating, reading, and managing CDS files. It acts as a service layer that interacts with `JGTCDS.py` to perform these operations.
  - The module provides functions to create CDS files from IDS datasets produced by `JGTIDS.py`, read CDS files, and manage the data. It also handles data cleansing and normalization.

* **Data Processing** 🔄
  - Raw PDS data is first transformed into IDS datasets by the `JGTIDS.py` service. This service adds the core indicator columns required by the rest of the system.
  - `JGTCDSSvc.py` calls into `JGTCDS.py`, which appends CDS‑specific columns such as fractal divergent bar signals, zero line cross signals, and zone signals.
  - The resulting dataset is cleansed and normalized to ensure it is ready for analysis and charting.

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

For more details, you can refer to the implementation in `jgtpy/JGTCDSSvc.py`, `jgtpy/JGTCDS.py`, and `jgtpy/JGTIDS.py`. The columns are also wrapped in `jgtpy/jgtcli.py`.
