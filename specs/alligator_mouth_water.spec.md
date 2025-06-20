# Alligator Mouth Water Analysis Specification

This module derives additional state columns from CDS data. It classifies the Alligator indicator's mouth behavior and price interaction.

## Inputs
The analyzer requires sequences of:
- `jaw`, `teeth`, `lips` values representing the Alligator lines
- `High` and `Low` prices for each bar
- `ao` oscillator values (optional but used for water state)

### Lookback Considerations
The analyzer inspects at least the last two bars to calculate slopes and
distances. Some trading setups may require additional **lagging features** from
earlier bars (for example three or more periods back) to confirm transitions.
The `lookback_periods` setting controls this history window and defaults to
**3**. Voice or CLI workflows may extend this lookback if deeper context proves
useful.

## Output Columns
After processing, the following columns are appended to the dataframe:
- `mouth_direction`: `buy`, `sell` or `neither`
- `mouth_phase`: `opening`, `open`, `closing`, `sleeping`, `none`
- `bar_position`: location of the bar relative to the mouth (`above`, `in`, `below`)
- `water_state`: activity classification such as `splashing`, `eating`, `throwing`, `poping`, `entering`, `switching`, `sleeping`
- `mouth_direction_confidence`: score between 0 and 1 for the direction calculation
- `mouth_phase_confidence`: score between 0 and 1 for the phase calculation
- `state_transition`: boolean marking when any of the states change

## Algorithm Highlights
1. **Mouth Direction** – Uses slope and line ordering of the three Alligator lines to decide buy/sell/neither. Confidence increases with separation and slope magnitude.
2. **Mouth Phase** – Evaluates the distance between lines or optionally a Gator Oscillator to decide whether the mouth is opening, open, closing or sleeping.
3. **Bar Position** – Compares the bar's high/low to the line extremes to decide above/in/below.
4. **Water State** – Combines direction, phase, and bar position with AO momentum to produce the water activity state. Transition detection compares with the previous bar state.

## Usage
`analyze_dataframe(df)` attaches these columns to a CDS dataframe. The results
are consumed by `mouth_water_plotter` and ADS plotting routines.

## Operational Context
CLI tools schedule this analysis periodically (e.g. every five minutes) and feed
the enriched dataset into plotting or voice-based inspection loops. During a
time-boxed observation window—usually around ninety seconds—an agent describes
the latest mouth and water states in natural language. These descriptions map
back into programmatic triggers for trading decisions or alerts.
