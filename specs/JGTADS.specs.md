# JGTADS Charting Specification

This document describes the plotting logic of `JGTADS.py` in implementation independent terms. It outlines the required data columns and how they are used to build each subplot so another language can reproduce the same visuals.

## Required Data Structure

The input is a tabular dataset (CSV or DataFrame) produced by the CDS service. It combines all columns documented in `IDS_data_columns.md` and `CDS_data_columns.md`. Key fields used by the charting routine are:

- **OHLC columns**: `Open`, `High`, `Low`, `Close` (price series for candlesticks).
- **Alligator lines**: `jaw`, `teeth`, `lips`.
- **Fractals**: `fh`, `fl` plus optional degree variants `fh<n>` and `fl<n>` where `<n>` indicates fractal degree (e.g. `fh8`).
- **FDB signals**: `fdb`, `fdbb`, `fdbs`.
- **AO/AC oscillators**: `ao`, `ac`.
- **Saucer and peak markers**: `sb`, `ss`, `price_peak_above`, `price_peak_bellow`, `ao_peak_above`, `ao_peak_bellow`.
- **Zone information**: `zcol`, `zlc`, `zlcB`, `zlcS`.
- **Mouth/Water state**: `mouth_direction`, `mouth_phase`, `bar_position`, `water_state`, `mouth_direction_confidence`, `mouth_phase_confidence`.

All rows are indexed by date/time which is converted to the appropriate format depending on timeframe.

## Plot Layout

The routine builds a multi‑panel figure using mplfinance:

1. **Main panel** – OHLC bars and overlays.
   - Candles are colored by `zcol` (zone color).
   - Alligator lines (`jaw`, `teeth`, `lips`) are drawn as separate lines.
   - Fractal markers (regular, higher degree, and ultra) are plotted using the `fh*` and `fl*` columns with slight vertical offsets.
   - Divergent bar signals (`fdbb` and `fdbs`) appear as scatter markers above or below the bar.
   - Price peak markers and mouth water annotations (from `mouth_*` columns) can be added when enabled.
2. **AO panel** – Awesome Oscillator bar chart with optional saucer signals and AO peak markers.
3. **AC panel** – Acceleration/Deceleration Oscillator bar chart with optional AC buy/sell markers.

Additional subplots are only rendered if the corresponding `JGTChartConfig` flags are true. The figure title shows the instrument and timeframe with a subtitle displaying the last bar time and bar count.

## Plotting Steps

1. **Data Selection**: keep the latest `nb_bar_on_chart` rows from the dataset so the plot window size matches the chart config.
2. **Color/offset calculations**: dynamic offsets are computed from average bar height to place markers above or below candles without overlap. AO and AC colors depend on bar-to-bar delta.
3. **Addplots construction**: each optional indicator produces one or more `addplot` objects describing scatter or line series. These are accumulated and supplied to `mpf.plot`.
4. **Figure decoration**: after plotting, the subtitle, axis limits, and grid settings are adjusted. Future bars space is added on the right.
5. **Saving and display**: figures can be saved to disk or displayed on screen based on the request flags.

## Usage Notes

- `JGTChartConfig` controls which overlays appear. Disabling AO hides the AO panel and shifts AC up.
- The mouth/water annotations rely on analysis results from `alligator_mouth_water.py`. If those columns are absent, the plot is generated without them.
- The plotting code expects data sorted by ascending datetime with no gaps.

This specification allows implementing an equivalent chart generator in another environment while keeping behavior consistent with the Python version.
