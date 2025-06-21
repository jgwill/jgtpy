# JGTChartConfig Specification

This configuration object controls how ADS charts are rendered. Another language can reproduce ADS visuals by respecting the fields described here.

## Key Parameters
- **nb_bar_on_chart**: Number of bars to display in the main window.
- **cds_required_amount_of_bar_for_calc**: Minimum history needed for indicator calculations.
- **show_ao, show_ac**: Toggle AO and AC panels. When AO is disabled, AC shifts to the second panel.
- **show_fractal**, **show_fractal_higher**, **show_fractal_ultra_higher**: Enable different fractal levels.
- **show_fdb_signal**: Display divergent bar markers.
- **show_price_peak**, **show_saucer**, **show_ao_peaks**: Additional signal overlays.
- **show_alligator**: Plot Alligator lines.
- **show_zlc**: Show zero line cross data on the AO panel.
- **plot_style**: mplfinance style name (e.g. "yahoo").
- **main_plot_type**: Candle or ohlc bar type.
- **marker sizes and colors**: Many attributes define marker size and color for each indicator. These should map directly to plotting library styles.

## Behavior
Calling `update()` adjusts dependent flags so that feature presets like `show_plain_plot` or `show_feature_one_plot` alter multiple other options. Implementations should replicate this logic when applying presets.

`new_feature_plot(feature_plot)` returns a preconfigured instance for demo charts. Feature 1 enables higher fractals and FDB signals; feature 3 focuses on AC indicators, etc.

The configuration is typically accessed via `JGTADSRequest.cc` but can also be used standalone.
