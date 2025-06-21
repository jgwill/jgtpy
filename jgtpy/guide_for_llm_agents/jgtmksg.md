# jgtmksg - Market Signal Generation

Advanced signal generation system for creating trading alerts and market analysis based on CDS data.

## Console Command
```bash
jgtmksg -i INSTRUMENT -t TIMEFRAME [OPTIONS]
```

## Parameters
- `-i, --instrument` - Trading pair (e.g., EUR/USD, GBP/USD, USD/JPY)
- `-t, --timeframe` - Period (m1, m5, m15, m30, H1, H4, D1)
- `-c, --count` - Number of bars to analyze
- `-v, --verbose` - Verbosity level

## Usage Examples

### Basic Signal Generation
```bash
# Generate market signals
jgtmksg -i EUR/USD -t m5 -c 100

# With detailed verbosity
jgtmksg -i EUR/USD -t m5 -c 100 -v 1
```

### Multi-Timeframe Signals
```bash
# Short-term signals
jgtmksg -i GBP/USD -t m1 -c 500

# Medium-term signals
jgtmksg -i GBP/USD -t m15 -c 200

# Long-term signals  
jgtmksg -i GBP/USD -t H4 -c 100
```

### Different Instruments
```bash
# Major pairs analysis
jgtmksg -i EUR/USD -t m5 -c 200
jgtmksg -i GBP/USD -t m5 -c 200
jgtmksg -i USD/JPY -t m5 -c 200
```

## Signal Types Generated

### Bill Williams Signals
- Alligator crossover signals
- Awesome Oscillator momentum changes
- Accelerator saucer formations
- Fractal breakout alerts

### Zone-Based Signals
- Zone change notifications (buy/sell/neutral)
- Zone persistence analysis
- Multi-timeframe zone alignment

### Market State Signals
- Mouth direction changes
- Water state transitions
- Bar position shifts
- Confidence threshold alerts

## Output Format
Generates structured signal data including:
- Signal timestamp and type
- Signal strength/confidence
- Recommended action (buy/sell/hold)
- Supporting indicator values
- Risk assessment information

## Data Requirements
Requires CDS files with full analysis. Generate with:
```bash
jgtcli -i EUR/USD -t m5 -c 200 -ba -ta -mw
```

## Integration Workflow
```bash
# 1. Generate comprehensive data
jgtcli -i EUR/USD -t m5 -c 300 -ba -ta -mw

# 2. Create signal analysis
jgtmksg -i EUR/USD -t m5 -c 300 -v 1

# 3. Visualize signals with charts
jgtads -i EUR/USD -t m5 -c 300 -ba -ta -mw

# 4. Detailed state analysis
jgtmouthwater -i EUR/USD -t m5 -c 300 --show
```

## Signal Filtering
The system provides intelligent filtering to:
- Reduce false signals
- Focus on high-confidence opportunities
- Align with overall market structure
- Consider multi-timeframe context

## Use Cases
- Automated trading system alerts
- Manual trading decision support
- Market scanning and screening
- Risk management signal generation
- Multi-instrument portfolio analysis 