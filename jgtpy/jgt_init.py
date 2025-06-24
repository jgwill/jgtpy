#!/usr/bin/env python3
"""
JGT Trading Environment Initializer

Similar to 'npm init', this tool creates a new trading environment with
all necessary scripts, configuration, and documentation.
"""

import argparse
import os
import sys
import shutil
import json
from pathlib import Path
from datetime import datetime

def create_trading_environment(target_dir: str, name: str = None, interactive: bool = True):
    """Create a new trading environment"""

    target_path = Path(target_dir)
    if not target_path.exists():
        target_path.mkdir(parents=True, exist_ok=True)

    # Default name if not provided
    if name is None:
        name = target_path.name

    print(f"🚀 Creating JGT Trading Environment: {name}")
    print(f"📁 Location: {target_path.absolute()}")
    print()

    # Create directory structure
    directories = [
        "data/current/cds",
        "data/current/ids",
        "data/current/pds",
        "data/full/cds",
        "data/full/ids",
        "data/full/pds",
        "logs",
        "config",
        "scripts"
    ]

    for dir_path in directories:
        (target_path / dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {dir_path}")

    # Create configuration files
    create_config_files(target_path, name, interactive)

    # Install scripts
    install_scripts(target_path)

    # Create README
    create_readme(target_path, name)

    # Create environment file
    create_env_file(target_path)

    print()
    print("🎉 Trading environment created successfully!")
    print()
    print("Next steps:")
    print("1. cd", target_path.name)
    print("2. ./scripts/setup-service.sh --full")
    print("3. ./scripts/check-status.sh")
    print("4. ./scripts/refresh-all.sh")
    print()
    print("For help:")
    print("  guidecli_jgtpy --examples")
    print("  guidecli_jgtpy --section jgtservice")

def create_config_files(target_path: Path, name: str, interactive: bool):
    """Create configuration files"""

    # Trading configuration
    config = {
        "name": name,
        "created": datetime.now().isoformat(),
        "version": "1.0.0",
        "description": f"JGT Trading Environment: {name}",
        "instruments": ["EUR/USD", "XAU/USD", "GBP/USD", "USD/JPY", "SPX500", "USD/CAD",
        "AUD/CAD", "AUD/USD"],
        "timeframes": ["m5", "m15", "H1", "H4", "D1", "W1", "M1"],
        "settings": {
            "max_workers": 4,
            "refresh_interval": 300,
            "web_port": 8080,
            "enable_upload": False
        }
    }

    if interactive:
        print("\n📝 Configuration Setup:")
        instruments = input("Instruments (comma-separated, default: EUR/USD,XAU/USD,GBP/USD,USD/JPY): ").strip()
        if instruments:
            config["instruments"] = [i.strip() for i in instruments.split(",")]

        timeframes = input("Timeframes (comma-separated, default: m5,m15,m30,H1,H4,D1): ").strip()
        if timeframes:
            config["timeframes"] = [t.strip() for t in timeframes.split(",")]

        max_workers = input("Max workers (default: 4): ").strip()
        if max_workers and max_workers.isdigit():
            config["settings"]["max_workers"] = int(max_workers)

        web_port = input("Web API port (default: 8080): ").strip()
        if web_port and web_port.isdigit():
            config["settings"]["web_port"] = int(web_port)

    # Write config files
    config_file = target_path / "config" / "trading.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"✅ Created: config/trading.json")

    # Create settings file
    settings = {
        "data_path": str(target_path / "data" / "current"),
        "data_full_path": str(target_path / "data" / "full"),
        "logs_path": str(target_path / "logs"),
        "max_workers": config["settings"]["max_workers"],
        "web_port": config["settings"]["web_port"],
        "refresh_interval": config["settings"]["refresh_interval"]
    }

    settings_file = target_path / "config" / "settings.json"
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=2)
    print(f"✅ Created: config/settings.json")

def install_scripts(target_path: Path):
    """Install scripts to the scripts directory"""

    # Import the guide system to get script installation
    try:
        from .jgtpy_guide_for_agent import install_scripts
        installed, failed = install_scripts(str(target_path / "scripts"), overwrite=True)

        if installed:
            print(f"✅ Installed {len(installed)} scripts to scripts/")
        if failed:
            print(f"⚠️  Failed to install: {len(failed)} scripts")

    except ImportError:
        print("⚠️  Could not install scripts automatically")
        print("   Run: guidecli_jgtpy --install-scripts scripts/")

def create_readme(target_path: Path, name: str):
    """Create a README for the trading environment"""

    readme_content = f"""# {name} - JGT Trading Environment

This is a JGT trading environment created with `jgt init`.

## Quick Start

```bash
# Setup the service
./scripts/setup-service.sh --full

# Check status
./scripts/check-status.sh

# Refresh data
./scripts/refresh-all.sh

# Start API server
./scripts/start-api-server.sh
```

## Directory Structure

```
{name}/
├── config/           # Configuration files
├── data/            # Trading data
│   ├── current/     # Current data
│   └── full/        # Historical data
├── logs/            # Log files
└── scripts/         # JGT service scripts
```

## Configuration

- `config/trading.json` - Trading environment configuration
- `config/settings.json` - Service settings
- `.env` - Environment variables (create this)

## Environment Variables

Create a `.env` file with:

```bash
JGTPY_DATA={target_path}/data/current
JGTPY_DATA_FULL={target_path}/data/full
JGTPY_SERVICE_MAX_WORKERS=4
JGTPY_SERVICE_WEB_PORT=8080
```

## API Access

Once the service is running:

- Health: http://localhost:8080/api/v1/health
- Data: http://localhost:8080/api/v1/data/EUR/USD/H1
- Docs: http://localhost:8080/docs

## Help

- `guidecli_jgtpy --examples` - Script examples
- `guidecli_jgtpy --section jgtservice` - Service documentation
- `./scripts/check-status.sh --help` - Status check help

Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    readme_file = target_path / "README.md"
    with open(readme_file, 'w') as f:
        f.write(readme_content)
    print(f"✅ Created: README.md")

def create_env_file(target_path: Path):
    """Create a sample .env file"""

    env_content = f"""# JGT Trading Environment Configuration
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Data paths
JGTPY_DATA={target_path}/data/current
JGTPY_DATA_FULL={target_path}/data/full

# Timeframe configuration
TRADABLE_TIMEFRAMES=m5,m15,m30,H1,H4,D1
HIGH_TIMEFRAMES=H4,D1,W1
LOW_TIMEFRAMES=m5,m15,m30

# Service configuration
JGTPY_SERVICE_MAX_WORKERS=4
JGTPY_SERVICE_WEB_PORT=8080
JGTPY_SERVICE_REFRESH_INTERVAL=300

# Processing options
JGTPY_SERVICE_USE_FRESH=true
JGTPY_SERVICE_CONTINUE_ON_ERROR=true

# Upload configuration (optional)
JGTPY_SERVICE_ENABLE_UPLOAD=false
# JGTPY_DROPBOX_APP_TOKEN=your_token_here

# Security (optional)
# JGTPY_API_KEY=your_api_key_here
"""

    env_file = target_path / ".env"
    with open(env_file, 'w') as f:
        f.write(env_content)
    print(f"✅ Created: .env")

def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new JGT trading environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  jgt init                    # Create in current directory
  jgt init my-trading         # Create 'my-trading' directory
  jgt init /path/to/trading   # Create in specific path
  jgt init --no-interactive   # Use defaults, no prompts
        """
    )

    parser.add_argument('name', nargs='?', help='Name of the trading environment')
    parser.add_argument('--no-interactive', action='store_true', help='Use defaults, no prompts')
    parser.add_argument('--version', action='version', version='jgt init 1.0.0')

    args = parser.parse_args()

    # Determine target directory
    if args.name:
        if os.path.isabs(args.name):
            target_dir = args.name
            name = Path(args.name).name
        else:
            target_dir = args.name
            name = args.name
    else:
        target_dir = os.getcwd()
        name = Path(target_dir).name

    try:
        create_trading_environment(target_dir, name, not args.no_interactive)
    except KeyboardInterrupt:
        print("\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
