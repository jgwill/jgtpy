# JGTCDS Data Pipeline Specification

This document describes how the `JGTCDS.py` module consumes IDS data and produces Chaos Data Service (CDS) files. The goal is to capture the high-level steps so other implementations can replicate the logic.

## Inputs
- **IDS dataset** produced by `JGTIDS.py`.
- Each row represents a market bar with the indicator columns documented in `docs/IDS_data_columns.md`.

## Processing Steps
1. **Additional Indicators** – append CDS-specific columns such as fractal divergent bar signals, zero line cross signals and zone labels.
2. **Data Cleansing** – remove invalid rows, normalize column names and ensure timestamps are sorted.
3. **File Creation** – write the enriched dataset to a CDS file alongside optional zone data files.

## Outputs
- A CDS file (CSV/Parquet) containing all IDS columns plus the new CDS-specific ones.
- Optional zone files with aggregated zone data.

The module expects the IDS preprocessing to be complete before running. It does not calculate the base indicators itself but relies entirely on `JGTIDS.py`.
