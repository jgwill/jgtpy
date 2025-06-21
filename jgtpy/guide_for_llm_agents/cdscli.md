# cdscli - CDS Data Generation (Simplified)

Streamlined command for creating Chaos Data Service (CDS) datasets without extensive indicator calculations.

## Console Command
```bash
cdscli -i INSTRUMENT -t TIMEFRAME [OPTIONS]
```

## Parameters
- `-i, --instrument` - Trading pair (e.g., EUR/USD, GBP/USD, USD/JPY)
- `-t, --timeframe` - Period (m1, m5, m15, m30, H1, H4, D1)
- `-c, --count` - Number of bars to process
- `-v, --verbose` - Verbosity level

## Usage Examples

### Basic CDS Creation
```bash
# Simple dataset creation
cdscli -i EUR/USD -t m5 -c 100

# Multiple instruments
cdscli -i GBP/USD -t m15 -c 200
cdscli -i USD/JPY -t H1 -c 100
```

### Batch Processing
```bash
# Different timeframes for same instrument
cdscli -i EUR/USD -t m5 -c 500
cdscli -i EUR/USD -t m15 -c 200
cdscli -i EUR/USD -t H1 -c 100
```

## Comparison with jgtcli

### Use cdscli when:
- You need basic OHLCV data quickly
- No advanced indicators required
- Batch processing multiple instruments
- Simple data pipeline setup

### Use jgtcli when:
- Full technical analysis needed
- Bill Williams indicators required
- Mouth/water state analysis needed
- Comprehensive trading system development

```bash
# cdscli - Basic data
cdscli -i EUR/USD -t m5 -c 100

# jgtcli - Enhanced data
jgtcli -i EUR/USD -t m5 -c 100 -ba -ta -mw
```

## Output
Creates basic CDS files with:
- OHLCV price data
- Basic zone classification
- Volume information (when available)
- Standardized CSV format

## File Location
```
/workspace/data/current/cds/[INSTRUMENT]_[TIMEFRAME].csv
```

## Integration
Output files can be used by:
- `jgtads` for basic charting
- Further processing with `jgtcli` to add indicators
- Direct analysis in pandas environments
- Custom analysis scripts

## Performance
Faster than `jgtcli` due to minimal calculations, ideal for:
- Data pipeline initialization
- Quick dataset creation
- Testing and development
- Multi-instrument batch processing
