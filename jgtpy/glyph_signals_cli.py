#!/usr/bin/env python
"""Glyph-based CLI for indicator signals."""
import argparse
import pandas as pd

from jgtpy.alligator_mouth_water import load_cds_data


class SignalGlyphMapper:
    """Map indicator signal columns to glyphs."""

    signal_glyphs = {
        "fdbb": "🟢",  # fractal divergent bar buy
        "fdbs": "🔴",  # fractal divergent bar sell
        "fdb": "🎯",  # generic divergent bar
        "zlcb": "⬆️",  # zero line cross buy
        "zlcs": "⬇️",  # zero line cross sell
        "zlcB": "⬆️",  # legacy column
        "zlcS": "⬇️",  # legacy column
        "acb": "🔺",  # AC oscillator buy
        "acs": "🔻",  # AC oscillator sell
        "zone_sig": "💠",  # zone signal
    }

    ascii_glyphs = {
        "fdbb": "B",
        "fdbs": "S",
        "fdb": "F",
        "zlcb": "+",
        "zlcs": "-",
        "zlcB": "+",
        "zlcS": "-",
        "acb": "U",
        "acs": "D",
        "zone_sig": "O",
    }

    def __init__(self, style: str = "emoji") -> None:
        self.style = style

    def map_row(self, row: pd.Series, signals=None) -> str:
        if signals is None:
            signals = self.signal_glyphs.keys()
        mapping = self.ascii_glyphs if self.style == "ascii" else self.signal_glyphs
        glyphs = []
        for s in signals:
            key = s.lower()
            glyph = mapping.get(key)
            if glyph is None:
                glyph = mapping.get(s)
            if glyph is None:
                continue
            val = row.get(s)
            if val is None:
                val = row.get(key)
            if val is None:
                val = row.get(key.capitalize())
            if val:
                glyphs.append(glyph)
        default = "-" if self.style == "ascii" else "🪥"
        return "".join(glyphs) if glyphs else default


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
        default="fdbb,fdbs,zlcb,zlcs,acb,acs,zone_sig",
        help="Comma-separated signal columns to include",
    )
    p.add_argument(
        "--style",
        choices=["emoji", "ascii"],
        default="emoji",
        help="Glyph style to use",
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
    mapper = SignalGlyphMapper(style=args.style)
    tail_df = df.tail(args.n_bars)
    for ts, row in tail_df.iterrows():
        glyphs = mapper.map_row(row, signals)
        print(f"{ts}: {glyphs}")


if __name__ == "__main__":
    main()
