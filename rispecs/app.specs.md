# JGTpy Application Specification

> Master specification for the JGT Data Services Package

**Specification Version**: 1.0  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: A complete data transformation pipeline that converts raw price data into signal-rich trading intelligence, enriched with Williams 5 Dimensions indicators and ready for analysis.

**Achievement Indicator**: Users can run `cdscli --fresh` and obtain CDS files containing all Williams indicators, trading signals (FDB, ZLC, Saucer, Zone), and chart-ready data.

**Value Proposition**: Transform scattered price data into actionable trading signals through a systematic pipeline: PDS → IDS → CDS → ADS.

---

## Application Overview

JGTpy is a Python package that:
1. Wraps jgtfxcon for price data acquisition (PDS)
2. Enriches data with Williams indicators via jgtapy (IDS)
3. Generates trading signals for entries/exits (CDS)
4. Produces charts and visualizations (ADS)
5. Runs as automated service with scheduling (jgtservice)

---

## Structural Tension

**Current Reality**: Raw OHLCV price data lacks the derived indicators and signals needed for Williams-based trading decisions.

**Desired State**: Complete signal-rich datasets ready for trading analysis, served through CLI, API, or automated daemon.

**Natural Progression**: Each layer builds upon the previous, transforming raw data into actionable intelligence: PDS → IDS → CDS → ADS.

---

## Data Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    JGTpy Data Pipeline                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐   │
│  │   PDS   │ →  │   IDS   │ →  │   CDS   │ →  │   ADS   │   │
│  │ (Price) │    │(Indicators)│  │(Signals) │   │(Charts) │   │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘   │
│       ↑              ↑              ↑              ↑        │
│   jgtfxcon       jgtapy         JGTCDS.py      JGTADS.py   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Layer Descriptions

| Layer | Module | Description | Key Columns Added |
|-------|--------|-------------|-------------------|
| PDS | JGTPDSRequest | Raw OHLCV from broker | Date, Open, High, Low, Close, Volume |
| IDS | JGTIDS | Williams indicators | jaw, teeth, lips, ao, ac, fh, fl, mfi |
| CDS | JGTCDS | Trading signals | fdb, fdbb, fdbs, zlcB, zlcS, bz, sz |
| ADS | JGTADS | Visualization data | Chart-ready format |

---

## Core Signals (CDS)

### Signal Reference

| Signal | Column | Description |
|--------|--------|-------------|
| FDB | fdb | Fractal Divergent Bar (buy=-1, sell=1) |
| FDBB | fdbb | FDB Buy signal |
| FDBS | fdbs | FDB Sell signal |
| ZLC | zlc | Zero Line Crossing |
| ZLCB | zlcB | ZLC Buy signal |
| ZLCS | zlcS | ZLC Sell signal |
| BZ | bz | Buy Zone signal |
| SZ | sz | Sell Zone signal |
| SB | sb | Saucer Buy signal |
| SS | ss | Saucer Sell signal |
| FS | fs | Fractal Sell |
| FB | fb | Fractal Buy |

### FDB Signal Logic

**Fractal Divergent Bar (FDB)** is the primary entry signal:

```python
# Buy FDB conditions:
# 1. Price makes new fractal low (fl set)
# 2. AO does NOT make new low (bullish divergence)
# 3. Bar close above teeth line (Alligator confirmation)

# Sell FDB conditions:
# 1. Price makes new fractal high (fh set)
# 2. AO does NOT make new high (bearish divergence)
# 3. Bar close below teeth line
```

---

## CLI Tools

### jgtcli - Price/Indicator Data

```bash
# Fetch fresh price data with indicators
jgtcli -i EUR/USD -t H4 --fresh

# Multiple instruments and timeframes
jgtcli -i "EUR/USD,SPX500" -t "H1,H4,D1" --fresh

# With specific bar count
jgtcli -i EUR/USD -t H4 -c 500
```

### cdscli - Signal Generation

```bash
# Generate fresh CDS (signals)
cdscli -i EUR/USD -t H4 --fresh

# All configured instruments/timeframes
cdscli --all --fresh

# Use cached IDS data
cdscli -i EUR/USD -t H4
```

### jgtads - Advanced Charts

```bash
# Display chart
jgtads -i EUR/USD -t H4 --show

# Save chart to file
jgtads -i EUR/USD -t H4 --save_figure charts/

# Auto-named by timeframe
jgtads -i EUR/USD -t H4 --save_figure charts/ --save_figure_as_timeframe
```

### jgtservice - Daemon Mode

```bash
# One-time refresh
jgtservice --refresh-once -i EUR/USD -t H1

# Continuous daemon
jgtservice --daemon --all

# Web API server
jgtservice --web --port 8080

# Check status
jgtservice --status
```

---

## Type Definitions

```python
from typing import Dict, Any, Optional, List
import pandas as pd
from dataclasses import dataclass

# Instrument format: "EUR/USD", "SPX500"
Instrument = str

# Timeframe format: "m1", "m5", "m15", "m30", "H1", "H4", "D1", "W1", "M1"
Timeframe = str

@dataclass
class CDSData:
    """Chaos Data Service record with signals"""
    instrument: Instrument
    timeframe: Timeframe
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    # Alligator
    jaw: float
    teeth: float
    lips: float
    # Oscillators
    ao: float
    ac: float
    # Fractals
    fh: Optional[float]  # Fractal high
    fl: Optional[float]  # Fractal low
    # Signals
    fdb: int        # -1=buy, 0=none, 1=sell
    fdbb: bool      # FDB buy
    fdbs: bool      # FDB sell
    zlcB: bool      # ZLC buy
    zlcS: bool      # ZLC sell
    bz: bool        # Buy zone
    sz: bool        # Sell zone
    # MFI
    mfi: float
    mfi_signal: str  # "green", "squat", "fade", "fake"

def create_cds(
    instrument: Instrument,
    timeframe: Timeframe,
    bars: int = 335
) -> pd.DataFrame: ...

def read_cds(
    instrument: Instrument,
    timeframe: Timeframe
) -> pd.DataFrame: ...

def refresh_cds(
    instruments: List[Instrument],
    timeframes: List[Timeframe],
    parallel: bool = True
) -> Dict[str, Any]: ...
```

---

## Creative Advancement Scenarios

### Scenario: Fresh Signal Generation

**Desired Outcome**: Up-to-date CDS with all Williams signals

**Current Reality**: User starts trading session

**Natural Progression**:
1. User runs: `cdscli -i EUR/USD -t H4 --fresh`
2. JGTCDS invokes JGTIDS for indicator calculation
3. JGTIDS calls jgtapy for Alligator, AO, AC, Fractals, MFI
4. JGTCDS applies signal detection logic
5. CDS file written: `$JGTPY_DATA/cds/EUR-USD_H4.csv`

**Resolution**: CDS contains all indicators + signals, ready for analysis

### Scenario: Automated Refresh Service

**Desired Outcome**: Data stays current without manual intervention

**Current Reality**: Need continuous updates during trading hours

**Natural Progression**:
1. Start daemon: `jgtservice --daemon --all`
2. Scheduler monitors timeframe completion
3. On H1 close (e.g., 14:00), triggers refresh
4. PDS→IDS→CDS pipeline runs for all instruments
5. Optional cloud sync to Dropbox

**Resolution**: All data files stay current automatically

### Scenario: Terminal Chart Display

**Desired Outcome**: Visual analysis of Williams patterns

**Current Reality**: Want to see Alligator and signals on chart

**Natural Progression**:
1. User runs: `jgtads -i EUR/USD -t H4 --show`
2. JGTADS loads CDS data
3. mplfinance renders candlestick chart
4. Alligator lines overlaid (Jaw, Teeth, Lips)
5. Signals marked on chart (FDB, ZLC, etc.)

**Resolution**: Interactive chart displays complete Williams analysis

---

## File Storage

```
$JGTPY_DATA/
├── pds/                 # Price Data Service
│   ├── EUR-USD_H4.csv
│   └── ...
├── ids/                 # Indicator Data Service (optional cache)
│   └── ...
├── cds/                 # Chaos Data Service (primary)
│   ├── EUR-USD_H4.csv
│   └── ...
└── ads/                 # Advanced Data (charts/exports)
    └── ...
```

---

## Module Structure

```
jgtpy/
├── __init__.py           # Package exports
├── jgtcli.py             # jgtcli entry point
├── cdscli.py             # cdscli entry point
├── JGTIDS.py             # Indicator Data Service
├── JGTIDSRequest.py      # IDS request handling
├── JGTIDSSvc.py          # IDS service layer
├── JGTCDS.py             # Chaos Data Service
├── JGTCDSRequest.py      # CDS request handling
├── JGTCDSSvc.py          # CDS service layer
├── JGTADS.py             # Advanced Data Service
├── JGTADSRequest.py      # ADS request handling
├── JGTPDHelper.py        # PD utilities
├── JGTPDSP.py            # PDS processing
├── JGTPDSRequest.py      # PDS request handling
├── jgtservice.py         # Daemon service
├── jgtapycli.py          # Indicator CLI
├── jgtapyhelper.py       # jgtapy integration
├── glyph_cli.py          # Terminal glyphs
├── alligator_mouth_water.py  # Alligator state analysis
└── service/              # Service components
```

---

## Integration with JGT Ecosystem

```
jgtcore (configuration)
    ↓
jgtutils (utilities)
    ↓
jgtapy (indicators)
    ↓
jgtfxcon (broker connection)
    ↓
jgtpy (this package) ← Central data layer
    ↓ provides CDS data
jgtml (ML/analysis)
    ↓
jgt-data-server (REST API)
    ↓
jgt-code (terminal agent)
```

---

## Quality Criteria

✅ **Complete Pipeline**: PDS→IDS→CDS→ADS fully implemented  
✅ **Williams Native**: All 5 Dimensions as first-class data  
✅ **CLI Complete**: Every operation available via command line  
✅ **Daemon Mode**: Automated refresh with scheduling  
✅ **Parallel Processing**: Multi-instrument concurrent refresh  
✅ **API Ready**: RESTful endpoints via jgtservice
