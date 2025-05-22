# Purpose of JGTCDS.py

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

For more details, you can refer to the implementation in `jgtpy/JGTCDS.py`, `jgtpy/JGTIDS.py`, and `jgtpy/JGTCDSSvc.py`. The columns are also wrapped in `jgtpy/jgtcli.py`.

# Purpose of JGTCDSSvc.py

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

For more details, you can refer to the implementation in `jgtpy/JGTCDSSvc.py`, `jgtpy/JGTCDS.py`, and `jgtpy/JGTIDS.py`. The columns are also wrapped in `jgtpy/jgtcli.py`.
