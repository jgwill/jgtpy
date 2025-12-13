# 🚀 JGTService Quick Start

**Simplest possible setup to get jgtservice running.**

---

## ⚡ 30-Second Setup

```bash
# 1. Create trading environment
jgt init my-trading

# 2. Enter directory
cd my-trading

# 3. Start service (one-time refresh)
jgtservice
```

Done. Data will be processed and placed in `data/current/cds/`.

---

## 📋 What You Need (Minimum)

1. **Instruments** - which pairs/assets to process
2. **Timeframes** - which timeframes (H1, D1, etc.)
3. **Data paths** - where to store processed data

**All provided by `jgt init`** with sensible defaults.

---

## 🎯 Common Commands

### Run Once (Default)
```bash
jgtservice
```
Process all instruments/timeframes once, then exit.

### Check Configuration
```bash
jgtservice --status
```
View current setup and validate configuration.

### Run in Daemon Mode
```bash
jgtservice --daemon
```
Continuous refresh on a schedule. Ctrl+C to stop.

### Use Fresh Data
```bash
jgtservice --fresh
```
Force regeneration of underlying market data.

### Custom Instruments/Timeframes
```bash
jgtservice -i EUR/USD -i XAU/USD -t H1 -t D1
```

---

## 🔧 Configuration Methods (Priority Order)

### 1. Command Line (Fastest)
```bash
jgtservice -i EUR/USD -t H1 --fresh
```

### 2. Environment Variables
```bash
export JGTPY_SERVICE_INSTRUMENTS="EUR/USD,XAU/USD"
export JGTPY_SERVICE_TIMEFRAMES="H1,D1"
jgtservice
```

### 3. `.env` File (in current directory)
```bash
JGTPY_SERVICE_INSTRUMENTS=EUR/USD,XAU/USD
JGTPY_SERVICE_TIMEFRAMES=H1,D1
```
Then: `jgtservice`

### 4. `~/.jgt/config.json` (Global)
```json
{
  "instruments": ["EUR/USD", "XAU/USD"],
  "timeframes": ["H1", "D1"],
  "settings": {
    "max_workers": 4
  }
}
```

---

## 🔄 Service Modes

| Mode | Command | Use Case |
|------|---------|----------|
| **Once** | `jgtservice` | Process data once, exit |
| **Daemon** | `jgtservice --daemon` | Continuous background refresh |
| **Web API** | `jgtservice --web` | REST API server (requires FastAPI) |
| **Status** | `jgtservice --status` | View configuration only |

---

## 📁 Generated Data

After running `jgtservice`:

```
my-trading/
└── data/
    ├── current/
    │   └── cds/           ← Processed market data
    └── full/
        └── cds/           ← Historical data (with --full flag)
```

Each file: `INSTRUMENT_TIMEFRAME.csv`
Example: `EUR_USD_H1.csv`

---

## ⚠️ Troubleshooting

**"No instruments configured"**
```bash
jgtservice -i EUR/USD -i XAU/USD
```

**"Dropbox token required"**
```bash
jgtservice --no-upload   # Disable cloud upload
```

**"Configuration validation failed"**
```bash
jgtservice --status      # See what's missing
```

---

## 🎓 Next Steps

1. **Process custom instruments:**
   ```bash
   jgtservice -i GBP/USD -i USD/JPY -t H4 -t D1
   ```

2. **Use full historical data:**
   ```bash
   jgtservice --full      # Generates complete history
   ```

3. **Check logs:**
   ```bash
   jgtservice --verbose
   ```

4. **Enable API server:**
   ```bash
   pip install jgtpy[serve]
   jgtservice --web --port 8080
   ```

---

## 🔗 Resources

- Full options: `jgtservice --help`
- Architecture details: see `/src/jgtpy/CLAUDE.md`
- Create environment: `jgt init --help`
