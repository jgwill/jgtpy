#!/usr/bin/env python
"""CLI entry point for FDB scanning based on strategy intent."""

import argparse
import sys

from intent_spec import load_strategy
from fdb_scanner import scan_fdb

try:
    import yaml
except Exception:
    yaml = None


def parse_args():
    parser = argparse.ArgumentParser(description="JGT Agentic CLI")
    parser.add_argument("-i", "--instrument", default="EUR/USD", help="Instrument symbol, comma separated")
    parser.add_argument("-t", "--timeframe", default="H1", help="Timeframe, comma separated")
    parser.add_argument("-s", "--strategy", help="Path to strategy YAML intent")
    parser.add_argument("-y", "--yaml", action="store_true", help="Output results as YAML")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress verbose output")
    return parser.parse_args()


def main():
    args = parse_args()

    instruments = args.instrument.split(",")
    timeframes = args.timeframe.split(",")

    if args.strategy:
        spec = load_strategy(args.strategy)
        if spec.instruments:
            instruments = spec.instruments
        if spec.timeframes:
            timeframes = spec.timeframes

    results = scan_fdb(instruments, timeframes, quiet=args.quiet)

    if args.yaml:
        if yaml is None:
            sys.exit("PyYAML is required for YAML output")
        print(yaml.safe_dump({"signals": results}, sort_keys=False))
    else:
        for r in results:
            status = "✅" if r["fdb"] else "-"
            print(f"{r['instrument']}_{r['timeframe']}: {status}")


if __name__ == "__main__":
    main()
