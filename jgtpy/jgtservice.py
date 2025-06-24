#!/usr/bin/env python
"""
JGT Data Refresh Service - Main CLI Entry Point

This script provides the main entry point for the JGT data refresh service with
automated scheduling, parallel processing, and cloud distribution capabilities.

Usage:
    jgtservice --daemon --timeframes "H1,m15" --instruments "EUR/USD,XAU/USD"
    jgtservice --web --port 8080
    jgtservice --refresh-once --all
    jgtservice --status
"""

import sys
import os
import argparse
import logging
from typing import List, Optional

# Add current directory to path for relative imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import from jgtutils for argument parsing and settings
from jgtutils import jgtcommon
from jgtutils.jgtclihelper import print_jsonl_message

# Import service components
from service.base import JGTServiceConfig, JGTServiceManager

logger = logging.getLogger(__name__)

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments for the service"""
    
    parser = jgtcommon.new_parser(
        "JGT Data Refresh Service",
        epilog="Automated data refresh service with timeframe scheduling and cloud distribution",
        enable_specified_settings=True
    )
    
    # Service mode arguments
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        '--daemon', '-d',
        action='store_true',
        help='Run in daemon mode with continuous timeframe-based refresh'
    )
    mode_group.add_argument(
        '--web', '-w', 
        action='store_true',
        help='Run web server mode with API endpoints'
    )
    mode_group.add_argument(
        '--refresh-once', '-r',
        action='store_true', 
        help='Run one-time data refresh and exit'
    )
    mode_group.add_argument(
        '--status', '-s',
        action='store_true',
        help='Show service status and configuration'
    )
    
    # Configuration arguments (made optional since --status doesn't need them)
    parser.add_argument(
        '-i', '--instrument',
        type=str,
        action='append',  # Allow multiple -i arguments
        help='Instrument to process (e.g., EUR/USD, XAU/USD). Can be specified multiple times.'
    )
    parser.add_argument(
        '-t', '--timeframe', 
        type=str,
        action='append',  # Allow multiple -t arguments
        help='Timeframe to process (e.g., H1, m15, H4). Can be specified multiple times.'
    )
    
    # Service-specific arguments
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Process all configured instruments and timeframes'
    )
    
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=8080,
        help='Port for web server mode (default: 8080)'
    )
    
    parser.add_argument(
        '--workers', '-j',
        type=int,
        default=4,
        help='Number of parallel workers (default: 4)'
    )
    
    parser.add_argument(
        '--no-upload',
        action='store_true',
        help='Disable cloud upload functionality'
    )
    
    # Processing options
    jgtcommon.add_use_fresh_argument(parser)
    jgtcommon.add_bars_amount_V2_arguments(parser)
    jgtcommon.add_verbose_argument(parser)
    
    # Upload configuration
    parser.add_argument(
        '--upload-path',
        type=str,
        help='Custom upload path for cloud storage'
    )
    
    return jgtcommon.parse_args(parser)


def create_config_from_args(args: argparse.Namespace) -> JGTServiceConfig:
    """Create service configuration from parsed arguments"""
    
    # Start with environment-based config
    config = JGTServiceConfig.from_env()
    
    # Override with command line arguments
    if hasattr(args, 'instrument') and args.instrument:
        if args.all:
            # Use all configured instruments
            pass  # Keep config.instruments from env/settings
        else:
            config.instruments = args.instrument
    
    if hasattr(args, 'timeframe') and args.timeframe:
        if args.all:
            # Use all configured timeframes  
            pass  # Keep config.timeframes from env/settings
        else:
            config.timeframes = args.timeframe
    
    # Service mode settings
    config.daemon_mode = getattr(args, 'daemon', False)
    config.web_mode = getattr(args, 'web', False)  
    config.refresh_once = getattr(args, 'refresh_once', False)
    
    # Other settings
    if hasattr(args, 'port'):
        config.web_port = args.port
    if hasattr(args, 'workers'):
        config.max_workers = args.workers
    if hasattr(args, 'no_upload'):
        config.enable_upload = not args.no_upload
    if hasattr(args, 'fresh'):
        config.use_fresh = args.fresh
    if hasattr(args, 'full'):
        config.use_full = args.full
    if hasattr(args, 'verbose'):
        config.verbose_level = args.verbose
        config.quiet = args.verbose == 0
    
    return config


def show_status(config: JGTServiceConfig):
    """Show current service configuration and status"""
    print("JGT Data Refresh Service - Configuration Status")
    print("=" * 50)
    print(f"Instruments: {', '.join(config.instruments)}")
    print(f"Timeframes: {', '.join(config.timeframes)}")
    print(f"Max Workers: {config.max_workers}")
    print(f"Data Path: {config.data_path}")
    print(f"Data Full Path: {config.data_full_path}")
    print(f"Upload Enabled: {config.enable_upload}")
    if config.enable_upload:
        print(f"Upload Path (Current): {config.upload_path_current}")
        print(f"Upload Path (Full): {config.upload_path_full}")
        print(f"Dropbox Token: {'SET' if config.dropbox_token else 'NOT SET'}")
    print(f"Use Fresh: {config.use_fresh}")
    print(f"Use Full: {config.use_full}")
    print(f"Verbose Level: {config.verbose_level}")
    
    # Validate configuration
    errors = config.validate()
    if errors:
        print("\nConfiguration Errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\nConfiguration: VALID")


def main():
    """Main entry point for the JGT service"""
    
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Create configuration
        config = create_config_from_args(args)
        
        # Handle status request
        if getattr(args, 'status', False):
            show_status(config)
            return
        
        # Set default mode if none specified
        if not any([config.daemon_mode, config.web_mode, config.refresh_once]):
            config.refresh_once = True
        
        # Create and start service
        service_manager = JGTServiceManager(config)
        
        logger.info("Starting JGT Data Refresh Service...")
        print_jsonl_message(
            "JGT Service starting",
            extra_dict={
                "mode": "daemon" if config.daemon_mode else "web" if config.web_mode else "once",
                "instruments": config.instruments,
                "timeframes": config.timeframes
            },
            scope="jgtservice",
            state="starting"
        )
        
        service_manager.start()
        
    except KeyboardInterrupt:
        logger.info("Service interrupted by user")
        print_jsonl_message(
            "JGT Service interrupted by user",
            scope="jgtservice", 
            state="interrupted"
        )
    except Exception as e:
        logger.error(f"Service failed: {e}")
        print_jsonl_message(
            f"JGT Service failed: {e}",
            scope="jgtservice",
            state="error"
        )
        sys.exit(1)


if __name__ == '__main__':
    main() 