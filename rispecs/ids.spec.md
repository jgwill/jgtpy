# IDS (Indicator Data Service) Specification

> Williams Trading System Indicator Calculations

**Specification Version**: 1.0  
**Module**: `jgtpy/JGTIDS.py`  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: DataFrames enriched with complete Bill Williams Trading System indicators - the mathematical foundation for Chaos Trading signals.

**Achievement Indicator**: Given a PDS DataFrame, produces DataFrame with:
- All Alligator variants (Regular, Big, Tide)
- Awesome Oscillator (AO) with color
- Accelerator Oscillator (AC) with color
- Fractals at multiple periods (3, 5, 8, 13, 21, 34, 55, 89)
- FDB signals and Zero Line Crosses

**Value Proposition**: Single function to add all Williams indicators - the computational core of the trading system.

---

## Structural Tension

**Current Reality**: Raw OHLCV price data with no analytical value.

**Desired State**: Price data with complete indicator suite enabling Williams Trading System analysis.

**Natural Progression**: OHLCV → Alligator → AO/AC → Fractals → FDB → ZLC → Zone.

---

## Core Function: ids_add_indicators

```python
def ids_add_indicators(
    dfsrc: pd.DataFrame,
    dropnavalue: bool = True,
    quiet: bool = True,
    cleanupOriginalColumn: bool = True,
    useLEGACY: bool = True,
    cc: JGTChartConfig = None,
    bypass_index_reset: bool = False,
    rq: JGTIDSRequest = None
) -> pd.DataFrame:
    """
    Add all Williams Trading System indicators to DataFrame.
    
    Args:
        dfsrc: DataFrame with OHLCV columns
        dropnavalue: Drop rows with NaN values
        quiet: Suppress console output
        cleanupOriginalColumn: Remove intermediate columns
        cc: Chart configuration (optional)
        rq: Request object with indicator flags
    
    Calculation Order:
        1. Alligator (Regular 5-8-13)
        2. Big Alligator (34-55-89) - if enabled
        3. Tide Alligator (144-233-377) - if enabled
        4. Awesome Oscillator
        5. Accelerator Oscillator
        6. Gator Oscillator - if enabled
        7. Fractals (multiple periods)
        8. FDB (Fractal Divergent Bar) signals
        9. Zero Line Cross signals
        10. Zone coloring
        11. MFI (Market Facilitation Index) - if enabled
        12. AO/Price peaks - if enabled
    
    Returns:
        DataFrame with all indicators added
    """
```

---

## IDS Request Object

```python
@dataclass
class JGTIDSRequest:
    """Configuration for indicator calculations."""
    
    # Alligator flags
    gator_oscillator_flag: bool = False
    balligator_flag: bool = False
    talligator_flag: bool = False
    
    # Alligator periods
    balligator_period_jaws: int = 89   # Big: 34-55-89
    talligator_period_jaws: int = 377  # Tide: 144-233-377
    
    # Feature flags
    mfi_flag: bool = True
    ao_peaks_flag: bool = False
    mouth_water_flag: bool = False
    
    # Fractal configuration
    largest_fractal_period: int = 89
    
    # Processing options
    quotescount: int = 300
    keep_bid_ask: bool = True
    dropna_volume: bool = True
```

---

## Alligator Calculation

### Regular Alligator (5-8-13)

```python
# Columns: jaw, teeth, lips
median = (High + Low) / 2

jaw = SMMA(median, period=13).shift(8)     # Blue line
teeth = SMMA(median, period=8).shift(5)    # Red line
lips = SMMA(median, period=5).shift(3)     # Green line

# SMMA = Smoothed Moving Average
# First value: SMA(period)
# Subsequent: (prev_smma * (period - 1) + current) / period
```

### Big Alligator (34-55-89)

```python
# Columns: bjaw, bteeth, blips
bjaw = SMMA(median, period=89).shift(8)
bteeth = SMMA(median, period=55).shift(5)
blips = SMMA(median, period=34).shift(3)
```

### Tide Alligator (144-233-377)

```python
# Columns: tjaw, tteeth, tlips
tjaw = SMMA(median, period=377).shift(8)
tteeth = SMMA(median, period=233).shift(5)
tlips = SMMA(median, period=144).shift(3)
```

---

## Awesome Oscillator (AO)

```python
def calculate_ao(df: pd.DataFrame) -> pd.Series:
    """
    Awesome Oscillator: 5-period SMA minus 34-period SMA of median price.
    
    Formula:
        median = (High + Low) / 2
        AO = SMA(median, 5) - SMA(median, 34)
    
    Color:
        aocolor = "green" if AO[i] > AO[i-1] else "red"
    """
    median = (df['High'] + df['Low']) / 2
    ao = median.rolling(5).mean() - median.rolling(34).mean()
    return ao
```

---

## Accelerator Oscillator (AC)

```python
def calculate_ac(df: pd.DataFrame) -> pd.Series:
    """
    Accelerator Oscillator: AO minus 5-period SMA of AO.
    
    Formula:
        AC = AO - SMA(AO, 5)
    
    Color:
        accolor = "green" if AC[i] > AC[i-1] else "red"
    """
    ao = df['ao']
    ac = ao - ao.rolling(5).mean()
    return ac
```

---

## Gator Oscillator

```python
def calculate_gator(df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
    """
    Gator Oscillator: Visual representation of Alligator convergence/divergence.
    
    Upper (Jaw-Teeth):
        gator_upper = abs(jaw - teeth)
        gator_upper_color = "green" if increasing else "red"
    
    Lower (Teeth-Lips):
        gator_lower = -abs(teeth - lips)  # Negative for display
        gator_lower_color = "green" if decreasing else "red"
    
    Phases:
        - Sleeping: Both bars decreasing
        - Awakening: One bar growing, one shrinking
        - Feeding: Both bars increasing
        - Sated: Both bars beginning to decrease
    """
```

---

## Fractal Calculation

```python
def calculate_fractals(
    df: pd.DataFrame,
    periods: List[int] = [3, 5, 8, 13, 21, 34, 55, 89]
) -> pd.DataFrame:
    """
    Calculate fractal highs and lows at multiple periods.
    
    Fractal High (period N):
        High[i] is highest of High[i-N//2:i+N//2+1]
        Must have N bars around it (centered)
    
    Fractal Low (period N):
        Low[i] is lowest of Low[i-N//2:i+N//2+1]
        Must have N bars around it (centered)
    
    Output Columns:
        fh, fl (5-bar default)
        fh3, fl3 (3-bar)
        fh5, fl5 (5-bar explicit)
        fh8, fl8 (8-bar)
        fh13, fl13 (13-bar)
        ...up to largest_fractal_period
    """
```

---

## FDB (Fractal Divergent Bar) Signals

```python
def calculate_fdb(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fractal Divergent Bar - Primary entry signal.
    
    FDB Buy Conditions (fdbb=1):
        1. Fractal Low present (fl=1)
        2. Bar closes above Alligator Teeth
        3. Low is below Alligator Teeth
        4. AO supports direction (green preferred)
    
    FDB Sell Conditions (fdbs=1):
        1. Fractal High present (fh=1)
        2. Bar closes below Alligator Teeth
        3. High is above Alligator Teeth
        4. AO supports direction (red preferred)
    
    Combined Signal:
        fdb = fdbb - fdbs  # 1=buy, -1=sell, 0=none
    """
```

---

## Zero Line Cross (ZLC)

```python
def calculate_zlc(df: pd.DataFrame) -> pd.DataFrame:
    """
    Zero Line Cross detection for AO.
    
    ZLC Buy (zlcb=1):
        AO crosses from negative to positive
        AO[i-1] < 0 and AO[i] >= 0
    
    ZLC Sell (zlcs=1):
        AO crosses from positive to negative
        AO[i-1] > 0 and AO[i] <= 0
    
    Combined:
        zlc = zlcb - zlcs
    """
```

---

## Zone Calculation

```python
def calculate_zone(df: pd.DataFrame) -> pd.DataFrame:
    """
    Zone coloring based on AO and AC momentum.
    
    Buying Zone (bz=1, zcol="B"):
        - 2+ consecutive green AO bars
        - AND 2+ consecutive green AC bars
        - Strong bullish momentum
    
    Selling Zone (sz=1, zcol="S"):
        - 2+ consecutive red AO bars
        - AND 2+ consecutive red AC bars
        - Strong bearish momentum
    
    Neutral Zone (zcol="N"):
        - Neither buying nor selling zone
        - Choppy/consolidating market
    
    zone_sig: Same as zcol for consistency
    """
```

---

## MFI (Market Facilitation Index)

```python
def calculate_mfi(df: pd.DataFrame) -> pd.DataFrame:
    """
    Market Facilitation Index classification.
    
    Formula:
        MFI = (High - Low) / Volume
    
    Classification (comparing to previous bar):
        Green: MFI up, Volume up (strong trend)
        Fade: MFI down, Volume down (trend exhaustion)
        Squat: MFI down, Volume up (battle, potential reversal)
        Fake: MFI up, Volume down (false move)
    
    Columns:
        mfi: Raw MFI value
        mfi_sig: Classification letter (G/F/S/K)
    """
```

---

## Column Constants

```python
# Regular Alligator
JAW = "jaw"
TEETH = "teeth"
LIPS = "lips"

# Big Alligator
BJAW = "bjaw"
BTEETH = "bteeth"
BLIPS = "blips"

# Tide Alligator
TJAW = "tjaw"
TTEETH = "tteeth"
TLIPS = "tlips"

# Oscillators
AO = "ao"
AC = "ac"
AOCOLOR = "aocolor"
ACCOLOR = "accolor"

# Fractals
FH = "fh"
FL = "fl"
FH3, FL3 = "fh3", "fl3"
FH5, FL5 = "fh5", "fl5"
# ... up to FH89, FL89

# Signals
FDB = "fdb"
FDBB = "fdbb"
FDBS = "fdbs"
ZLC = "zlc"
ZLCB = "zlcb"
ZLCS = "zlcs"

# Zone
BZ = "bz"
SZ = "sz"
ZCOL = "zcol"
ZONE_SIGNAL = "zone_sig"

# MFI
MFI = "mfi"
MFI_SIG = "mfi_sig"
```

---

## Helper Functions

```python
def normalize_columns(
    df: pd.DataFrame,
    columns: List[str],
    in_place: bool = True
) -> pd.DataFrame:
    """Normalize columns to [-1, 1] range for ML."""

def _jgtpd_col_add_range_shifting(
    dfsrc: pd.DataFrame,
    ctxcolname: str,
    colprefix: str,
    endrange: int
) -> pd.DataFrame:
    """Add shifted column versions for lag features."""
```

---

## Dependencies

```python
import pandas as pd
import numpy as np
from jgtapy import Indicators           # Core indicator library
from jgtutils.jgtconstants import *     # Column name constants
from JGTIDSRequest import JGTIDSRequest
from JGTChartConfig import JGTChartConfig
from aohelper import add_ao_price_peaks_v2
from alligator_mouth_water import AlligatorMouthWaterAnalyzer  # Optional
```

---

## Quality Criteria

✅ **Complete Williams Suite**: All 5 dimensions implemented  
✅ **Three Alligators**: Regular, Big, Tide with correct periods  
✅ **Multi-period Fractals**: 3, 5, 8, 13, 21, 34, 55, 89 bars  
✅ **Proper Shifts**: Alligator lines shifted correctly  
✅ **Color Coding**: AO/AC colors for visual analysis  
✅ **Zone Detection**: Buying/Selling zone identification
