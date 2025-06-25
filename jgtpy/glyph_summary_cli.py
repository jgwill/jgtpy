#!/usr/bin/env python
"""Glyph CLI combining mouth/water states and indicator signals."""
import argparse
import pandas as pd

from jgtpy.alligator_mouth_water import (
    load_cds_data,
    analyze_dataframe,
)
from jgtpy.glyph_cli import GlyphMapper
from jgtpy.glyph_signals_cli import SignalGlyphMapper


def _parse_args():
    p = argparse.ArgumentParser(
        description="Summarize mouth/water states and indicator signals with emoji glyphs",
        epilog="Outputs recent bars as glyph sequences",
    )
    p.add_argument("-i", "--instrument", required=True, help="Instrument symbol")
    p.add_argument("-t", "--timeframe", required=True, help="Timeframe code")
    p.add_argument("--n-bars", type=int, default=5, help="Number of bars to show")
    p.add_argument("--data-dir", default=None, help="CDS data directory")
    p.add_argument("--use-full", action="store_true", help="Load full dataset")
    p.add_argument("--show-position", action="store_true", help="Include bar position glyph")
    p.add_argument(
        "--signals",
        default="fdbb,fdbs,zlcB,zlcS,zone_sig",
        help="Comma-separated signal columns to include",
    )
    p.add_argument(
        "--style",
        choices=["emoji", "ascii"],
        default="emoji",
        help="Glyph style to use",
    )
    return p.parse_args()


class CombinedGlyphMapper:
    """Map both mouth/water states and indicator signals."""

    def __init__(self, show_position: bool = False, signals=None, style: str = "emoji"):
        self.state_mapper = GlyphMapper(style=style)
        self.signal_mapper = SignalGlyphMapper(style=style)
        self.show_position = show_position
        self.signals = signals
        self.style = style

    def map_row(self, row: pd.Series) -> str:
        state = self.state_mapper.map_row(row, show_position=self.show_position)
        signals = self.signal_mapper.map_row(row, self.signals)
        return f"{state} {signals}"


def main():
    args = _parse_args()
    df = load_cds_data(
        args.instrument,
        args.timeframe,
        data_dir=args.data_dir,
        use_full=args.use_full,
    )

    required_cols = {"mouth_direction", "mouth_phase", "water_state"}
    if not required_cols.issubset(df.columns):
        df = analyze_dataframe(df)

    signals = [s.strip() for s in args.signals.split(",") if s.strip()]
    mapper = CombinedGlyphMapper(
        show_position=args.show_position, signals=signals, style=args.style
    )
    tail_df = df.tail(args.n_bars)
    for ts, row in tail_df.iterrows():
        glyphs = mapper.map_row(row)
        print(f"{ts}: {glyphs}")


if __name__ == "__main__":
    main()
