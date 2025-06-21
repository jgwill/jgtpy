# JGTADSRequest Specification

`JGTADSRequest` represents a plotting request. It extends `JGTCDSRequest` to fetch data and holds a `JGTChartConfig` instance.

## Important Fields
- **instrument** and **timeframe**: Identifiers for the dataset to plot.
- **cc**: Embedded `JGTChartConfig` controlling plot appearance.
- **tlid_range**: Optional bar range selection when plotting events.
- **nb_bar_on_chart**, **cds_required_amount_of_bar_for_calc**, **nb_bar_to_retrieve**: Mirrored from the config but can be overridden in the request constructor.
- **save_additional_figures_path** / **save_additional_figures_dpi**: Where to store images when requested.
- **show_feature_one_plot**, **show_plain_plot**, etc.: Convenience flags passed to `cc` so presets can be chosen directly when building requests.
- **plot_ao_peaks** and **show**: Additional runtime parameters for `JGTADS` plotting functions.

## Behavior
Creating a new request with `new_feature_plot(instrument, timeframe, feature_plot)` builds an appropriate `JGTChartConfig` using `JGTChartConfig.new_feature_plot` and attaches it to the request.

Calling `reset()` synchronizes fields from `cc` back to the request for backward compatibility.

This object is typically fed into `jgtxplot18c_231209` or other ADS routines where it governs data selection and plotting behavior.
