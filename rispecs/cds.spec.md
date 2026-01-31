# CDS (Chaos Data Service) Specification

> FDB Signal Generation and Williams Indicator Processing

**Specification Version**: 1.0  
**Modules**: `jgtpy/JGTCDS.py`, `jgtpy/JGTCDSSvc.py`, `jgtpy/cdscli.py`  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: CDS datasets containing price data enriched with complete Williams Trading System signals (FDB, ZLC, Fractals, Zone, MFI) ready for trading decisions.

**Achievement Indicator**: Running `cdscli -i EUR/USD -t H1` produces:
- CSV file with OHLCV + all Williams indicators
- FDB signals (fdbb=1, fdbs=1) marking entry opportunities
- Zone coloring (B=buying, S=selling, N=neutral)
- All three Alligator types (regular, big, tide)

**Value Proposition**: Transform raw price data into actionable Williams signals in one command.

---

## Structural Tension

**Current Reality**: PDS files with raw OHLCV price data.

**Desired State**: CDS files with complete Williams indicator suite and FDB signals.

**Natural Progression**: PDS → Add Alligator → Add AO/AC → Add Fractals → Add FDB → Add Zone → Save CDS.

---

## Data Pipeline Position

```
PDS → IDS → [CDS] → TTF → MLF → MX
             ↑
       Current stage
```

**Dependencies**: Requires PDS (price data) from jgtfxcon or cached files.

---

## Core Function: createFromPDSFileToCDSFile

```python
def createFromPDSFileToCDSFile(
    instrument: str,
    timeframe: str,
    columns_to_remove: List[str] = None,
    quiet: bool = True,
    tlid_range: str = None,
    use_full: bool = False,
    rq: JGTCDSRequest = None,
    use_fresh: bool = True,
    keep_bid_ask: bool = True,
    gator_oscillator_flag: bool = False,
    mfi_flag: bool = True,
    balligator_flag: bool = False,
    balligator_period_jaws: int = 89,
    largest_fractal_period: int = 89,
    talligator_flag: bool = False,
    talligator_period_jaws: int = 377,
    mouth_water_flag: bool = False,
    viewpath: bool = False,
    quotescount: int = 300,
    dropna_volume: bool = True
) -> Tuple[str, pd.DataFrame]:
    """
    Create CDS file from PDS source.
    
    Algorithm:
        1. Create JGTCDSRequest from parameters
        2. Load PDS data (fresh or cached)
        3. Apply indicators via JGTIDS
        4. Calculate FDB signals
        5. Calculate Zone coloring
        6. Write CDS to file
        7. Update zone cache
    
    Returns:
        (filepath, dataframe) - path to CDS file and the DataFrame
    
    Output Path:
        $JGTPY_DATA/cds/{instrument}_{timeframe}.csv
    """
```

---

## CDS Request Object

```python
@dataclass
class JGTCDSRequest:
    """Request configuration for CDS generation."""
    instrument: str = ""
    timeframe: str = ""
    quotescount: int = 300
    use_full: bool = False
    use_fresh: bool = True
    keep_bid_ask: bool = True
    dropna_volume: bool = True
    
    # Indicator flags
    gator_oscillator_flag: bool = False
    mfi_flag: bool = True
    balligator_flag: bool = False
    talligator_flag: bool = False
    mouth_water_flag: bool = False
    
    # Alligator periods
    balligator_period_jaws: int = 89
    talligator_period_jaws: int = 377
    largest_fractal_period: int = 89
    
    viewpath: bool = False
    
    def talligator_fix_quotescount(self):
        """Ensure enough bars for Tide Alligator calculation."""
        if self.talligator_flag:
            min_bars = self.talligator_period_jaws * 2
            if self.quotescount < min_bars:
                self.quotescount = min_bars
```

---

## CLI Interface

```python
# jgtpy/cdscli.py

def main():
    """
    CDS CLI Entry Point.
    
    Arguments:
        -i, --instrument: Instrument symbol (required)
        -t, --timeframe: Timeframe (required)
        --fresh: Force fresh data fetch
        --full: Use full historical data
        -n, --quotescount: Number of bars
        --mfi: Include MFI indicator (default: True)
        --gator: Include Gator Oscillator
        --balligator: Include Big Alligator (89)
        --talligator: Include Tide Alligator (377)
        --mouth-water: Include Mouth Water analysis
        --largest-fractal-period: Fractal lookback period
        --viewpath: Show output path only
        --dropna-volume: Drop zero-volume bars
        --ads: Show chart after generation
    
    Examples:
        # Default CDS generation
        cdscli -i EUR/USD -t H1
        
        # Multiple instruments/timeframes
        cdscli -i EUR/USD,GBP/USD -t H1,H4
        
        # Include all Alligators
        cdscli -i SPX500 -t D1 --balligator --talligator
        
        # Fresh data with chart display
        cdscli -i GBPUSD -t H4 --fresh --ads
    """
```

---

## Output Schema

### Complete CDS DataFrame

```python
{
    # Price Data
    "Date": datetime,        # Index
    "Open": float,
    "High": float,
    "Low": float,
    "Close": float,
    "Volume": int,
    
    # Bid/Ask (optional)
    "BidOpen": float,
    "BidHigh": float,
    "BidLow": float,
    "BidClose": float,
    "AskOpen": float,
    "AskHigh": float,
    "AskLow": float,
    "AskClose": float,
    
    # Regular Alligator (5-8-13)
    "jaw": float,            # 13-period SMMA, shift 8
    "teeth": float,          # 8-period SMMA, shift 5
    "lips": float,           # 5-period SMMA, shift 3
    
    # Big Alligator (34-55-89) - if enabled
    "bjaw": float,
    "bteeth": float,
    "blips": float,
    
    # Tide Alligator (144-233-377) - if enabled
    "tjaw": float,
    "tteeth": float,
    "tlips": float,
    
    # Awesome Oscillator
    "ao": float,             # 5-34 SMA difference on medians
    "aocolor": str,          # "green" or "red"
    
    # Accelerator Oscillator
    "ac": float,             # AO - 5-period SMA of AO
    "accolor": str,          # "green" or "red"
    
    # Fractals
    "fh": int,               # Fractal High (1 or 0)
    "fl": int,               # Fractal Low (1 or 0)
    "fh3": int,              # 3-bar fractal high
    "fl3": int,              # 3-bar fractal low
    "fh5": int,              # 5-bar fractal high
    "fl5": int,              # 5-bar fractal low
    
    # Divergent Bars (FDB signals)
    "fdb": int,              # -1 (sell), 0 (none), 1 (buy)
    "fdbb": int,             # FDB Buy (1 or 0)
    "fdbs": int,             # FDB Sell (1 or 0)
    
    # Zero Line Cross
    "zlc": int,              # Zero line cross direction
    "zlcb": int,             # ZLC Buy
    "zlcs": int,             # ZLC Sell
    
    # Zone
    "bz": int,               # Buying zone (1 or 0)
    "sz": int,               # Selling zone (1 or 0)
    "zcol": str,             # Zone color: "B", "S", "N"
    "zone_sig": str,         # Zone signal
    
    # MFI (if enabled)
    "mfi": float,            # Market Facilitation Index
    "mfi_sig": str,          # MFI signal type
    
    # Bar characteristics
    "bar_height": float,     # High - Low
}
```

---

## Service Layer

```python
class JGTCDSSvc:
    """CDS Service for programmatic access."""
    
    @staticmethod
    def create(rq: JGTCDSRequest) -> pd.DataFrame:
        """Create CDS from request object."""
    
    @staticmethod
    def get(
        instrument: str,
        timeframe: str,
        use_full: bool = False,
        use_fresh: bool = True,
        quotescount: int = -1,
        quiet: bool = True,
        force_read: bool = False
    ) -> pd.DataFrame:
        """Get CDS, creating if needed."""
    
    @staticmethod
    def get_higher_cdf_datasets(
        instrument: str,
        timeframe: str,
        use_full: bool = False,
        use_fresh: bool = False,
        quotescount: int = -1,
        quiet: bool = True,
        force_read: bool = False
    ) -> Dict[str, pd.DataFrame]:
        """
        Get CDS for all timeframes higher than specified.
        Used by TTF for cross-timeframe analysis.
        
        Returns:
            {"H1": df, "H4": df, "D1": df, "W1": df, "MN": df}
        """
    
    @staticmethod
    def zone_update_from_cdf(
        instrument: str,
        timeframe: str,
        cdf: pd.DataFrame,
        quiet: bool = True
    ) -> Tuple[str, dict]:
        """Update zone cache from CDS DataFrame."""
```

---

## Indicator Calculation (JGTIDS)

```python
def ids_add_indicators(
    dfsrc: pd.DataFrame,
    dropnavalue: bool = True,
    quiet: bool = True,
    cleanupOriginalColumn: bool = True,
    cc: JGTChartConfig = None,
    rq: JGTIDSRequest = None
) -> pd.DataFrame:
    """
    Add Williams Trading System indicators to DataFrame.
    
    Calculation Order:
        1. Alligator (jaw, teeth, lips)
        2. Big Alligator (bjaw, bteeth, blips) - if enabled
        3. Tide Alligator (tjaw, tteeth, tlips) - if enabled
        4. Awesome Oscillator (ao, aocolor)
        5. Accelerator Oscillator (ac, accolor)
        6. Gator Oscillator - if enabled
        7. Fractals (fh, fl, fh3, fl3, fh5, fl5)
        8. FDB signals (fdb, fdbb, fdbs)
        9. Zero Line Cross (zlc, zlcb, zlcs)
        10. Zone (bz, sz, zcol)
        11. MFI - if enabled
        12. AO/Price peaks - if enabled
    
    Returns:
        DataFrame with all indicators added
    """
```

---

## Williams Five Dimensions

### 1. Fractal (Space)
```python
# Fractal High: High[i-2] < High[i] > High[i+2] for 5-bar
# Fractal Low: Low[i-2] > Low[i] < Low[i+2] for 5-bar
```

### 2. Momentum (AO)
```python
# AO = SMA(median, 5) - SMA(median, 34)
# median = (High + Low) / 2
# aocolor = "green" if AO > AO[-1] else "red"
```

### 3. Acceleration (AC)
```python
# AC = AO - SMA(AO, 5)
# accolor = "green" if AC > AC[-1] else "red"
```

### 4. Zone
```python
# Buying Zone: 2+ consecutive green AO AND 2+ consecutive green AC
# Selling Zone: 2+ consecutive red AO AND 2+ consecutive red AC
# Neutral: Neither condition met
```

### 5. Balance Line (Alligator)
```python
# Jaw: SMMA(median, 13), shifted 8 bars
# Teeth: SMMA(median, 8), shifted 5 bars
# Lips: SMMA(median, 5), shifted 3 bars
```

---

## FDB Signal Logic

```python
def calculate_fdb(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Fractal Divergent Bar signals.
    
    FDB Buy (fdbb=1):
        - Fractal Low present (fl=1)
        - Close > Teeth
        - Bar forms below Alligator teeth
        - AO conditions met (green preferred)
    
    FDB Sell (fdbs=1):
        - Fractal High present (fh=1)
        - Close < Teeth
        - Bar forms above Alligator teeth
        - AO conditions met (red preferred)
    
    fdb = fdbb - fdbs  # Combined: 1 (buy), -1 (sell), 0 (none)
    """
```

---

## File Locations

```python
# CDS output paths:
$JGTPY_DATA/cds/{instrument}_{timeframe}.csv       # Current
$JGTPY_DATA_FULL/cds/{instrument}_{timeframe}.csv  # Full historical

# Zone cache:
$JGTPY_DATA/zone/{instrument}_{timeframe}.json
```

---

## Dependencies

```python
import pandas as pd
from jgtpy import JGTIDS as ids
from jgtpy import JGTPDSP as pds
from jgtapy import Indicators
from jgtutils.jgtos import get_data_path, mk_fullpath
from jgtutils import jgtconstants as c
from JGTCDSRequest import JGTCDSRequest
from JGTChartConfig import JGTChartConfig
```

---

## Quality Criteria

✅ **Complete Williams Suite**: All 5 dimensions calculated  
✅ **FDB Signals**: Entry signals with fractal + AO confirmation  
✅ **Three Alligators**: Regular (5-8-13), Big (34-55-89), Tide (144-233-377)  
✅ **Zone Coloring**: Buying/Selling/Neutral zones identified  
✅ **MFI Analysis**: Market Facilitation Index classification  
✅ **Service Layer**: Programmatic API for integrations
