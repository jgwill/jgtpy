# Glyph CLI Specification

This spec describes a small command line tool for summarizing market states with glyphs.

## Purpose
- Transform alligator mouth and water analysis into short emoji sequences.
- Useful for quick voice or text prompts where full charts are unnecessary.

## Required Data
- Dataset must include `mouth_direction`, `mouth_phase`, and `water_state` columns.
- If these columns are absent, the CLI will run `alligator_mouth_water.analyze_dataframe` on raw CDS data first.

## Arguments
- `-i/--instrument` – Instrument symbol (e.g. `EUR/USD`).
- `-t/--timeframe` – Timeframe code (e.g. `H1`).
- `--n-bars` – Number of recent bars to display (default: 5).
- `--data-dir` – Optional path to CDS data.
- `--use-full` – Load the full dataset from the CDS directory.
- `--show-position` – Append a glyph showing if the bar closed above, inside or below the mouth.
- `--style` – Choose `emoji` (default) or `ascii` glyph output.

## Behavior
1. Load CDS data with `alligator_mouth_water.load_cds_data`.
2. Ensure mouth/water columns exist by running `analyze_dataframe` when needed.
3. Map each row's states to a sequence of emoji glyphs:
   - 🐊 – alligator entry marker.
   - 💧 – water oscillation representation.
   - 📈 – direction or momentum cue.
   - 🏊 – active water state.
   - 🦷 – mouth logic (open/close).
   - 🪥 – reset or sleeping phase.
   - Position glyphs:
     - 📈 – price bar above the mouth.
     - 💧 – price within the mouth.
     - 🏊 – price below the mouth.
4. Print a timestamp and the glyph sequence for the requested number of bars.
5. When `--style ascii` is selected, use simple letters like `S`, `E`, `T` for
   water states and `+`/`-` for direction instead of emojis.

The output provides a condensed view of market conditions suitable for chat interfaces or quick logs.
