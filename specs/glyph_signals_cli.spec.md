# Glyph Signals CLI Specification

This spec defines a command line tool that translates key indicator signals into short emoji sequences.

## Purpose
- Provide a fast overview of fractal divergent bar and other signals.
- Useful for chat-based summaries when charts are unnecessary.

## Required Data
- CDS dataset containing signal columns such as `fdbb`, `fdbs`, `zlcb`, `zlcs`, `acb`, `acs`, and `zone_sig`.

## Arguments
- `-i/--instrument` – Instrument symbol.
- `-t/--timeframe` – Timeframe code.
- `--n-bars` – Number of bars to display (default: 5).
- `--data-dir` – Optional CDS directory path.
- `--use-full` – Load the full dataset rather than the recent subset.
- `--signals` – Comma-separated list of signal columns to display.
- `--style` – Choose `emoji` (default) or `ascii` glyph output.

## Behavior
1. Load CDS data with `load_cds_data` from `alligator_mouth_water.py`.
2. For each row, map active signal columns to emoji glyphs:
   - `fdbb` or `fdb` → 🐊 (divergent bar)
   - `fdbs` → 🦷 (divergent bar sell)
   - `zlcb` → 📈 (zero line cross buy)
   - `zlcs` → 🏊 (zero line cross sell)
   - `acb` → 🔺 (AC oscillator buy)
   - `acs` → 🔻 (AC oscillator sell)
   - `zone_sig` → 💧 (zone signal)
3. If no signals are active, output 🪥 as a neutral glyph.
4. When `--style ascii` is used, map signals to simple letters instead of emoji.
5. Print the timestamp with the glyph string for the requested number of bars.

The CLI allows quick signal checks through emoji, making it suitable for voice assistants or minimal interfaces.
