"""What jgwill/jgtsrc consumes from jgtpy. A change that fails here breaks jgtsrc.

Consumer, 2026-09-25: jgt-pricedb-util/src/jgtpricedb_util/jobs/derive_cds.py
(JgtpyIndicatorEngine), which the jgtsrc updater runs in its CDS workers:
    pds2cds.build_cds_request(instrument=..., timeframe=...)
    pds2cds.cds.createFromDF(prices, quiet=True, rq=request)
    pds2cds.svc.zone_update_from_cdf(instrument, timeframe, cds, quiet=True)
and, for the store's raw AO (jgwill/jgtsrc#159), request.normalize_ao_ac.

Run against the installed package: pytest tests/test_jgtsrc_contract.py
"""
import subprocess
import sys

import numpy as np
import pandas as pd

QUOTES = ["BidOpen", "BidHigh", "BidLow", "BidClose", "AskOpen", "AskHigh", "AskLow", "AskClose"]


def _prices(n=1000, seed=7):
    """A D1-like frame shaped like a jgtsrc price export: Date index, bid/ask and OHLC."""
    rng = np.random.default_rng(seed)
    mid = 1.10 + np.cumsum(rng.normal(0, 0.004, n))
    high = mid + rng.uniform(0.001, 0.006, n)
    low = mid - rng.uniform(0.001, 0.006, n)
    opn = low + (high - low) * rng.uniform(0, 1, n)
    close = low + (high - low) * rng.uniform(0, 1, n)
    df = pd.DataFrame({
        "BidOpen": opn, "BidHigh": high, "BidLow": low, "BidClose": close,
        "AskOpen": opn + 0.0001, "AskHigh": high + 0.0001, "AskLow": low + 0.0001, "AskClose": close + 0.0001,
        "Volume": rng.integers(1000, 5000, n),
    }, index=pd.date_range("2022-01-03 21:00", periods=n, freq="D", name="Date"))
    for c in ("Open", "High", "Low", "Close"):
        df[c] = (df[f"Bid{c}"] + df[f"Ask{c}"]) / 2
    df["Median"] = (df["High"] + df["Low"]) / 2
    return df


def _build(prices, **request_attrs):
    from jgtpy import pds2cds
    rq = pds2cds.build_cds_request(instrument="EUR/USD", timeframe="D1")
    for k, v in request_attrs.items():
        setattr(rq, k, v)
    return pds2cds.cds.createFromDF(prices.copy(), quiet=True, rq=rq)


def test_importing_pds2cds_leaves_the_plotting_stack_unloaded():
    code = ("import sys; from jgtpy import pds2cds; "
            "print(sorted(m for m in ('matplotlib', 'panel', 'bokeh') if m in sys.modules))")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert out.stdout.strip().splitlines()[-1] == "[]"


def test_the_derive_cds_surface_exists():
    from jgtpy import pds2cds
    rq = pds2cds.build_cds_request(instrument="EUR/USD", timeframe="D1")
    assert rq.normalize_ao_ac is True
    assert callable(pds2cds.cds.createFromDF)
    assert callable(pds2cds.svc.zone_update_from_cdf)


def test_a_placeholder_candle_changes_nothing():
    prices = _prices()
    dirty = prices.copy()
    row = dirty.index[-300]
    dirty.loc[row, QUOTES + ["Open", "High", "Low", "Close", "Median"]] = 1.0
    clean = _build(prices.drop(index=row))
    out = _build(dirty)
    assert out.shape == clean.shape
    assert np.allclose(out.select_dtypes("number"), clean.select_dtypes("number"), equal_nan=True)


def test_raw_ao_is_the_default_ao_times_one_divisor():
    prices = _prices()
    norm = _build(prices)
    raw = _build(prices, normalize_ao_ac=False)
    both = (norm["ao"] != 0) & (raw["ao"] != 0)
    ratio = norm["ao"][both] / raw["ao"][both]
    assert ratio.max() - ratio.min() < 1e-3 * ratio.median()
    assert raw["ao"].abs().max() < 0.2  # price units, not a -1..1 scale
