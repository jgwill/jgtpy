# jgtids - Indicator Data Service Analysis

Specialized command for generating and analyzing Indicator Data Service (IDS) files with focused technical indicator calculations.

## Console Commands
```bash
# Primary modern command
jgtids -i INSTRUMENT -t TIMEFRAME [OPTIONS]

# Legacy equivalent
idscli -i INSTRUMENT -t TIMEFRAME [OPTIONS]
```

## Parameters
- `-i, --instrument` - Trading pair (e.g., EUR/USD, GBP/USD, USD/JPY)
- `-t, --timeframe` - Period (m1, m5, m15, m30, H1, H4, D1)
- `-c, --count` - Number of bars to process
- `-v, --verbose` - Verbosity level

## Usage Examples

### Basic Indicator Analysis
```bash
# Generate IDS file with standard indicators
jgtids -i EUR/USD -t m5 -c 100

# With detailed output
jgtids -i EUR/USD -t m5 -c 100 -v 1
```

### Multi-Timeframe Indicator Analysis
```bash
# Short-term indicators
jgtids -i GBP/USD -t m1 -c 500

# Medium-term indicators  
jgtids -i GBP/USD -t m15 -c 200

# Long-term indicators
jgtids -i GBP/USD -t H4 -c 100
```

### Batch Indicator Processing
```bash
# Multiple instruments analysis
jgtids -i EUR/USD -t m5 -c 200
jgtids -i GBP/USD -t m5 -c 200
jgtids -i USD/JPY -t m5 -c 200
```

## Indicator Types Generated

### Core Technical Indicators
- Moving averages (various periods)
- RSI (Relative Strength Index)
- MACD components
- Stochastic oscillators
- Bollinger Bands

### Bill Williams Focused
- Alligator lines with precise calculations
- Awesome Oscillator refined values
- Accelerator Oscillator detailed analysis
- Fractal identification and marking

### Volume Analysis
- Volume-based indicators
- Money Flow Index (MFI)
- Volume rate of change
- Volume-price trend analysis

## Output Format
Creates specialized IDS files containing:
- High-precision indicator calculations
- Normalized indicator values
- Signal strength metrics
- Indicator divergence detection
- Multi-timeframe indicator alignment

## Data Source
Can work with:
- Existing CDS files (preferred)
- Raw price data (PDS format)
- Real-time broker feeds

```bash
# Generate base data first
jgtcli -i EUR/USD -t m5 -c 200 -ba

# Then create focused indicator analysis
jgtids -i EUR/USD -t m5 -c 200
```

## Integration with Other Commands

### Combined Analysis Workflow
```bash
# 1. Generate base CDS data
jgtcli -i EUR/USD -t m5 -c 300 -ba

# 2. Create detailed indicator analysis
jgtids -i EUR/USD -t m5 -c 300

# 3. Generate trading signals
jgtmksg -i EUR/USD -t m5 -c 300

# 4. Create comprehensive charts
jgtads -i EUR/USD -t m5 -c 300 -ba
```

## Specialized Features
- High-precision calculations for indicator accuracy
- Indicator correlation analysis
- Multi-timeframe indicator synchronization
- Custom indicator parameter optimization
- Signal quality assessment

## Use Cases
- Indicator backtesting and optimization
- Signal generation system development
- Multi-timeframe analysis
- Indicator performance comparison
- Custom trading system validation

## Output Location
```
/workspace/data/current/ids/[INSTRUMENT]_[TIMEFRAME].csv
```
