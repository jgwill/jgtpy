# JGTADS Charting Specification

This document describes the plotting logic of `JGTADS.py` in implementation independent terms. It outlines the required data columns and how they are used to build each subplot so another language can reproduce the same visuals.

## Required Data Structure

The input is a tabular dataset (CSV or DataFrame) produced by the CDS service. It contains price series, indicator lines and numerous derived signals used for plotting.

### Price and Volume
- `Date` – timestamp of each bar
- `BidOpen`, `BidHigh`, `BidLow`, `BidClose` – raw bid prices
- `AskOpen`, `AskHigh`, `AskLow`, `AskClose` – raw ask prices
- `Open`, `High`, `Low`, `Close` – consolidated OHLC values
- `Volume` – tick volume
- `Median` – midpoint of High and Low

### Core Indicators
- `ao` – Awesome Oscillator
- `ac` – Acceleration/Deceleration Oscillator
- `jaw`, `teeth`, `lips` – Alligator lines
- `bjaw`, `bteeth`, `blips` – baseline Alligator averages
- `tjaw`, `tteeth`, `tlips` – trailing Alligator averages
- `mfi` – Market Facilitation Index

### Fractal Levels
- `fh`, `fl` – base fractal highs and lows
- `fh3`, `fl3`, `fh5`, `fl5`, `fh8`, `fl8`, `fh13`, `fl13`, `fh21`, `fl21`, `fh34`, `fl34`, `fh55`, `fl55`, `fh89`, `fl89` – higher degree fractals

### Signals and Zones
- `fdb`, `fdbb`, `fdbs` – fractal divergent bar signals
- `aoaz`, `aobz` – AO zone classification
- `zlc`, `zlcb`, `zlcs` – zero line cross values
- `zcol` – zone color
- `zone_sig` – zone signal label
- `bz`, `sz` – buy and sell zone flags
- `acs`, `acb` – AC oscillator buy/sell markers
- `ss`, `sb` – saucer sell/buy markers
- `price_peak_above`, `price_peak_bellow` – price peak markers
- `ao_peak_above`, `ao_peak_bellow` – AO peak markers

### Mouth/Water States
- `mouth_direction`, `mouth_phase`, `bar_position`, `water_state`
- `mouth_direction_confidence`, `mouth_phase_confidence`

### Additional MFI Metrics
- `mfi_sq`, `mfi_green`, `mfi_fade`, `mfi_fake`, `mfi_sig`, `mfi_str`

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

## Output
The plotting routine returns a figure object, the associated axes list and the clipped dataset used for the plot. Implementations may instead stream the figure to a web interface or save it to disk depending on the request settings.

This specification allows implementing an equivalent chart generator in another environment while keeping behavior consistent with the Python version.
