# Mouth Water Plotter Specification

This specification captures the behavior of `mouth_water_plotter.py`. The module visualizes the Alligator mouth state analysis produced by `alligator_mouth_water.py`.

## Data Requirements

The plotter expects the CDS dataset to include the following columns for each bar:

- `mouth_direction` – buy, sell or neither.
- `mouth_phase` – opening, open, closing, sleeping, none.
- `bar_position` – relative location of the bar to the mouth: above, in or below.
- `water_state` – classified price action: splashing, eating, throwing, poping, entering, switching or sleeping.
- `mouth_direction_confidence` – confidence score of the direction estimate.
- `mouth_phase_confidence` – confidence score of the phase estimate.

OHLC columns (`High`, `Low`) are also needed for placing markers.

## Plot Outputs

The plotter can produce two kinds of output:

1. **Addplots for integration with JGTADS** – `create_mouth_water_addplots` returns a list of mplfinance `addplot` objects representing water state and mouth direction symbols overlaid on the main chart. A special highlight is drawn for the last completed bar.
2. **Standalone analysis charts** – `create_specialized_mouth_water_chart` can generate dedicated views such as a states timeline, last state analysis, or a combined zone/state visualization.

## Symbol Mapping

Markers are selected according to configuration:

- Water states map to colored symbols or emojis (fallback to ASCII for compatibility).
- Mouth direction uses triangle markers; bar position uses triangles or squares.
- Colors reflect buy/sell/neutral interpretation.

Marker sizes and offsets are configurable via `MouthWaterPlotConfig`.

## Workflow

1. Instantiate `MouthWaterPlotter` with optional configuration.
2. Call `create_mouth_water_addplots(data, panel_id)` to get overlays for the main ADS plot.
3. Optional: use `create_specialized_mouth_water_chart` for more detailed standalone visuals or CLI output.
   Ensure the input dataset is ordered by time so markers appear in the correct sequence.

These steps allow any implementation to reproduce the same overlay and analysis charts using the data columns described above.
