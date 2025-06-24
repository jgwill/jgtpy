#!/usr/bin/env python
"""Glyph-based CLI for indicator signals."""
import argparse
import pandas as pd

from jgtpy.alligator_mouth_water import load_cds_data


class SignalGlyphMapper:
    """Map indicator signal columns to emoji glyphs."""

    signal_glyphs = {
        "fdbb": "🐊",  # fractal divergent bar buy
        "fdbs": "🦷",  # fractal divergent bar sell
        "zlcB": "📈",  # zero line cross buy
        "zlcS": "🏊",  # zero line cross sell
        "zone_sig": "💧",  # zone signal
    }

    def map_row(self, row: pd.Series, signals=None) -> str:
        if signals is None:
            signals = self.signal_glyphs.keys()
        glyphs = [self.signal_glyphs[s] for s in signals if s in row and row[s]]
        return "".join(glyphs) if glyphs else "🪥"


def _parse_args():
    p = argparse.ArgumentParser(
        description="Summarize indicator signals with emoji glyphs",
        epilog="Outputs recent bars as a sequence of glyphs",
    )
    p.add_argument("-i", "--instrument", required=True, help="Instrument symbol")
    p.add_argument("-t", "--timeframe", required=True, help="Timeframe code")
    p.add_argument("--n-bars", type=int, default=5, help="Number of bars to show")
    p.add_argument("--data-dir", default=None, help="CDS data directory")
    p.add_argument("--use-full", action="store_true", help="Load full dataset")
    p.add_argument(
        "--signals",
        default="fdbb,fdbs,zlcB,zlcS,zone_sig",
        help="Comma-separated signal columns to include",
    )
    return p.parse_args()


def main():
    args = _parse_args()
    df = load_cds_data(
        args.instrument,
        args.timeframe,
        data_dir=args.data_dir,
        use_full=args.use_full,
    )

    signals = [s.strip() for s in args.signals.split(",") if s.strip()]
    mapper = SignalGlyphMapper()
    tail_df = df.tail(args.n_bars)
    for ts, row in tail_df.iterrows():
        glyphs = mapper.map_row(row, signals)
        print(f"{ts}: {glyphs}")


if __name__ == "__main__":
    main()
