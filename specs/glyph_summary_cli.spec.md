# Glyph Summary CLI Specification

This spec describes a command line tool that outputs emoji sequences summarizing both Alligator mouth/water states and key indicator signals.

## Purpose
- Combine the visual cues from `glyphcli` and `signalglyph` into a single output.
- Useful for quick overviews when both state and signal context matter.

## Required Data
- CDS dataset with mouth/water columns (`mouth_direction`, `mouth_phase`, `water_state`).
- Indicator signal columns like `fdbb`, `fdbs`, `zlcB`, `zlcS`, and `zone_sig`.
- If mouth/water columns are missing, run `analyze_dataframe` to compute them.

## Arguments
- `-i/--instrument` – Instrument symbol.
- `-t/--timeframe` – Timeframe code.
- `--n-bars` – Number of recent bars to display (default: 5).
- `--data-dir` – Optional path to CDS data directory.
- `--use-full` – Load the full dataset instead of the recent subset.
- `--show-position` – Include a glyph for bar position relative to the mouth.
- `--signals` – Comma-separated list of signal columns to include.
- `--style` – Choose `emoji` (default) or `ascii` glyph output.

## Behavior
1. Load CDS data via `load_cds_data`.
2. Ensure mouth and water columns exist by running `analyze_dataframe` when necessary.
3. For each row, generate two glyph strings:
   - Mouth/water glyphs from `GlyphMapper` (and position glyph if requested).
   - Signal glyphs from `SignalGlyphMapper` for the selected signals.
4. Print the timestamp followed by the combined glyph string for the requested bars.
5. When `--style ascii` is chosen, both state and signal glyphs use simple characters instead of emojis.

This CLI allows voice interfaces or logs to display condensed market context using a short sequence of emoji glyphs.
