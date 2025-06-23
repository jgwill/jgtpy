#!/usr/bin/env python
"""Glyph-based market interpreter CLI."""
import argparse
import pandas as pd

from jgtpy.alligator_mouth_water import (
    MouthDirection,
    MouthPhase,
    WaterState,
    load_cds_data,
    analyze_dataframe,
)


def _parse_args():
    p = argparse.ArgumentParser(
        description="Summarize mouth and water states with emoji glyphs",
        epilog="Outputs recent bars as a sequence of glyphs",
    )
    p.add_argument("-i", "--instrument", required=True, help="Instrument symbol")
    p.add_argument("-t", "--timeframe", required=True, help="Timeframe code")
    p.add_argument("--n-bars", type=int, default=5, help="Number of bars to show")
    p.add_argument("--data-dir", default=None, help="CDS data directory")
    p.add_argument("--use-full", action="store_true", help="Load full dataset")
    return p.parse_args()


class GlyphMapper:
    """Map mouth and water states to a glyph sequence."""

    water_glyphs = {
        WaterState.SPLASHING: "🏊",
        WaterState.EATING: "💧",
        WaterState.THROWING: "📈",
        WaterState.POPING: "📈",
        WaterState.ENTERING: "🐊",
        WaterState.SWITCHING: "🪥",
        WaterState.SLEEPING: "🪥",
    }

    phase_glyphs = {
        MouthPhase.OPENING: "🦷",
        MouthPhase.OPEN: "🦷",
        MouthPhase.CLOSING: "🦷",
        MouthPhase.SLEEPING: "🪥",
        MouthPhase.NONE: "🪥",
    }

    direction_glyphs = {
        MouthDirection.BUY: "📈",
        MouthDirection.SELL: "📈",
        MouthDirection.NEITHER: "",
    }

    def map_row(self, row: pd.Series) -> str:
        direction = self.direction_glyphs.get(MouthDirection(row["mouth_direction"]), "")
        phase = self.phase_glyphs.get(MouthPhase(row["mouth_phase"]), "")
        water = self.water_glyphs.get(WaterState(row["water_state"]), "")
        return f"🐊{water}{phase}{direction}"


def main():
    args = _parse_args()
    df = load_cds_data(
        args.instrument,
        args.timeframe,
        data_dir=args.data_dir,
        use_full=args.use_full,
    )

    required_cols = {'mouth_direction', 'mouth_phase', 'water_state'}
    if not required_cols.issubset(df.columns):
        df = analyze_dataframe(df)

    mapper = GlyphMapper()
    tail_df = df.tail(args.n_bars)
    for ts, row in tail_df.iterrows():
        glyphs = mapper.map_row(row)
        print(f"{ts}: {glyphs}")


if __name__ == "__main__":
    main()
