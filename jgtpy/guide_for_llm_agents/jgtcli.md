# jgtcli - Main Data Generation CLI

The primary command for generating enhanced CDS (Chaos Data Service) files with comprehensive technical analysis.

## Console Command
```bash
jgtcli -i INSTRUMENT -t TIMEFRAME [OPTIONS]
```

## Essential Parameters
- `-i, --instrument` - Trading pair (e.g., EUR/USD, GBP/USD, USD/JPY)
- `-t, --timeframe` - Period (m1, m5, m15, m30, H1, H4, D1)
- `-c, --count` - Number of bars to process (default: varies by timeframe)

## Key Options
- `-ba, --balligator_flag` - Enable Bill Williams Alligator analysis
- `-ta, --technical_analysis_flag` - Enable full technical indicator suite  
- `-mw, --mouth_water_flag` - Enable alligator mouth/water state analysis
- `-v, --verbose` - Verbosity level (0-2)

## Usage Examples

### Basic CDS Generation
```bash
# Simple CDS file creation
jgtcli -i EUR/USD -t m5 -c 100

# With verbosity for debugging
jgtcli -i EUR/USD -t m5 -c 100 -v 1
```

### Full Analysis Pipeline
```bash
# Complete analysis with all indicators
jgtcli -i EUR/USD -t m5 -c 500 -ba -ta -mw -v 1

# Multi-timeframe analysis
jgtcli -i GBP/USD -t H1 -c 200 -ba -ta
jgtcli -i GBP/USD -t m15 -c 800 -ba -ta
```

### Specialized Analysis
```bash
# Focus on Bill Williams indicators
jgtcli -i USD/JPY -t m30 -c 300 -ba

# Include mouth/water states for trend analysis
jgtcli -i EUR/GBP -t H4 -c 100 -ba -mw
```

## Output
Creates enhanced CSV files in `/workspace/data/current/cds/` with:
- Original OHLCV data
- Technical indicators (when -ta enabled)
- Alligator lines: jaw, teeth, lips (when -ba enabled)  
- Awesome Oscillator and Accelerator values
- Zone classifications: buy/sell/neutral
- Mouth/water states (when -mw enabled)

## Generated Columns
Base columns: BidOpen, BidHigh, BidLow, BidClose, AskOpen, AskHigh, AskLow, AskClose, Volume

With `-ba`: jaw, teeth, lips, ao, ac, ao_color, ac_color, ac_saucer, zone, zcol

With `-ta`: MFI indicators, additional volume analysis

With `-mw`: mouth_direction, mouth_phase, bar_position, water_state, confidence scores

## File Output Location
```
/workspace/data/current/cds/[INSTRUMENT]_[TIMEFRAME].csv
```

## Integration
Output files are used by:
- `jgtads` for chart generation
- `jgtmksg` for signal analysis  
- `jgtmouthwater` for specialized visualization
- Direct analysis in pandas/jupyter environments
