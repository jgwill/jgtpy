# jgtmouthwater - Alligator Mouth/Water State Visualization

Specialized plotting tool for visualizing alligator mouth and water states with symbol representation and zone analysis.

## Console Command
```bash
jgtmouthwater -i INSTRUMENT -t TIMEFRAME [OPTIONS]
```

## Parameters
- `-i, --instrument` - Trading pair (e.g., EUR/USD, GBP/USD)
- `-t, --timeframe` - Period (m1, m5, m15, m30, H1, H4, D1)
- `-c, --count` - Number of bars (default: 100)
- `-ct, --chart_type` - Chart type (last_state_analysis, states_timeline, zone_combined)
- `--show` - Display chart interactively
- `-mw, --mouth_water_flag` - Force mouth water analysis
- `-v, --verbose` - Verbosity level

## Chart Types

### 1. Last State Analysis (default)
Detailed 2x2 analysis focusing on the last completed bar:
```bash
jgtmouthwater -i EUR/USD -t m5 -c 50 --show
```

### 2. States Timeline  
4-panel evolution view showing state changes over time:
```bash
jgtmouthwater -i EUR/USD -t m5 -c 100 -ct states_timeline --show
```

### 3. Zone Combined
Price analysis with zone integration:
```bash
jgtmouthwater -i EUR/USD -t m5 -c 75 -ct zone_combined --show
```

## Symbol Legend

### Water States
- `s` - Splashing (active movement)
- `o` - Eating (consuming trend) 
- `X` - Throwing (rejecting movement)
- `^` - Popping (bursting action)
- `>` - Entering (beginning entry)
- `D` - Switching (changing state)
- `.` - Sleeping (dormant/quiet)

### Mouth Direction
- `^` - Buy direction (upward pressure)
- `v` - Sell direction (downward pressure)  
- `D` - Neither (neutral/indecisive)

### Bar Position
- `^` - Above (price above alligator)
- `s` - In (price within alligator)
- `v` - Below (price below alligator)

## Usage Examples

### Basic Analysis
```bash
# Quick last state check
jgtmouthwater -i EUR/USD -t m5 -c 30

# With chart display
jgtmouthwater -i EUR/USD -t m5 -c 50 --show
```

### Comprehensive Analysis
```bash
# Full timeline analysis
jgtmouthwater -i GBP/USD -t m15 -c 200 -ct states_timeline --show

# Zone-integrated analysis
jgtmouthwater -i USD/JPY -t H1 -c 100 -ct zone_combined --show -v 1
```

### Different Timeframes
```bash
# Short-term scalping analysis
jgtmouthwater -i EUR/USD -t m1 -c 500 -ct last_state_analysis

# Daily trend analysis  
jgtmouthwater -i GBP/USD -t D1 -c 50 -ct zone_combined --show
```

## Output Information
The command provides:
- Last completed bar state summary
- Symbol representation for quick identification
- Confidence scores for state determination
- Visual charts (when --show enabled)

Example output:
```
Last Completed Bar State:
  Direction: sell Phase: closing Position: in Water: sleeping
  Symbols: . v
```

## Data Requirements
Requires CDS files with mouth water analysis. Generate with:
```bash
jgtcli -i EUR/USD -t m5 -c 100 -mw
```

## Integration Workflow
```bash
# 1. Generate data with mouth water analysis
jgtcli -i EUR/USD -t m5 -c 200 -ba -mw

# 2. Create specialized visualization
jgtmouthwater -i EUR/USD -t m5 -c 200 -ct last_state_analysis --show

# 3. Compare with regular charts
jgtads -i EUR/USD -t m5 -c 200
```

## Focus on Last Completed Period
The analysis emphasizes the second-to-last bar (last completed period) rather than the current incomplete bar, providing more reliable state information for decision making. 