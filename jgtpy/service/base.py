"""
Base service classes for JGT Data Refresh Service

This module provides the core service management and configuration classes.
"""

import sys
import os
import signal
import threading
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
import json

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import from parent jgtpy package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from jgtutils import jgtcommon
from jgtutils.jgtclihelper import print_jsonl_message

# Try to import python-dotenv if available
try:
    from dotenv import load_dotenv
    _has_dotenv = True
except ImportError:
    _has_dotenv = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def load_env_files():
    """Load .env files from multiple locations"""
    if not _has_dotenv:
        return
    
    # Load .env files in order of precedence (last one wins)
    env_locations = [
        Path.home() / ".env",  # $HOME/.env
        Path.home() / ".jgt" / ".env",  # $HOME/.jgt/.env
        Path.cwd() / ".env"  # CWD/.env (highest precedence)
    ]
    
    for env_file in env_locations:
        if env_file.exists():
            logger.debug(f"Loading environment from: {env_file}")
            load_dotenv(env_file)

def load_jgt_config() -> Dict[str, Any]:
    """Load configuration from $HOME/.jgt/config.json"""
    config_file = Path.home() / ".jgt" / "config.json"
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load {config_file}: {e}")
    return {}

@dataclass
class JGTServiceConfig:
    """Configuration class for JGT Service"""
    
    # Core settings
    instruments: List[str] = field(default_factory=lambda: ["EUR/USD", "XAU/USD"])
    timeframes: List[str] = field(default_factory=lambda: ["H1", "m15"])
    refresh_interval: int = 60  # seconds
    max_workers: int = 4
    
    # Data paths
    data_path: str = "/tmp/jgtpy/data/current"
    data_full_path: str = "/tmp/jgtpy/data/full"
    
    # Service modes
    daemon_mode: bool = False
    web_mode: bool = False
    web_port: int = 8080
    refresh_once: bool = False
    
    # Upload settings
    enable_upload: bool = True
    dropbox_token: Optional[str] = None
    upload_path_current: str = "/dist/data/current/cds"
    upload_path_full: str = "/dist/data/full/cds"
    
    # Processing settings
    use_fresh: bool = True
    use_full: bool = False
    quiet: bool = False
    verbose_level: int = 1
    
    # Error handling
    retry_attempts: int = 3
    retry_delay: int = 30  # seconds
    continue_on_error: bool = True
    
    @classmethod
    def from_env(cls) -> "JGTServiceConfig":
        """Create configuration from environment variables and config files"""
        # Load .env files first
        load_env_files()
        
        # Load JGT config file
        jgt_config = load_jgt_config()
        
        config = cls()
        
        # Parse instruments from env
        instruments_env = os.getenv("JGTPY_SERVICE_INSTRUMENTS", 
                                   os.getenv("JGTPY_INSTRUMENTS"))
        if instruments_env:
            config.instruments = [i.strip() for i in instruments_env.split(",")]
        elif "instruments" in jgt_config:
            config.instruments = jgt_config["instruments"]
        
        # Parse timeframes from env  
        timeframes_env = os.getenv("JGTPY_SERVICE_TIMEFRAMES",
                                  os.getenv("TRADABLE_TIMEFRAMES", 
                                           os.getenv("LOW_TIMEFRAMES")))
        if timeframes_env:
            config.timeframes = [t.strip() for t in timeframes_env.split(",")]
        elif "timeframes" in jgt_config:
            config.timeframes = jgt_config["timeframes"]
        
        # Other settings
        config.data_path = os.getenv("JGTPY_DATA", config.data_path)
        config.data_full_path = os.getenv("JGTPY_DATA_FULL", config.data_full_path)
        config.dropbox_token = os.getenv("JGTPY_DROPBOX_APP_TOKEN")
        
        # Try to get dropbox token from jgt_config if not in env
        if not config.dropbox_token and "dropbox_token" in jgt_config:
            config.dropbox_token = jgt_config["dropbox_token"]
        
        # Numeric settings
        if os.getenv("JGTPY_SERVICE_PARALLEL_WORKERS"):
            config.max_workers = int(os.getenv("JGTPY_SERVICE_PARALLEL_WORKERS"))
        if os.getenv("JGTPY_SERVICE_REFRESH_INTERVAL"):
            config.refresh_interval = int(os.getenv("JGTPY_SERVICE_REFRESH_INTERVAL"))
        if os.getenv("JGTPY_SERVICE_WEB_PORT"):
            config.web_port = int(os.getenv("JGTPY_SERVICE_WEB_PORT"))
        
        # Boolean settings
        config.enable_upload = os.getenv("JGTPY_SERVICE_ENABLE_UPLOAD", "true").lower() == "true"
        config.use_fresh = os.getenv("JGTPY_SERVICE_USE_FRESH", "true").lower() == "true"
        config.use_full = os.getenv("JGTPY_SERVICE_USE_FULL", "false").lower() == "true"
        config.quiet = os.getenv("JGTPY_SERVICE_QUIET", "false").lower() == "true"
        
        return config
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of errors"""
        errors = []
        
        if not self.instruments:
            errors.append("No instruments configured")
        if not self.timeframes:
            errors.append("No timeframes configured")
        if self.max_workers < 1:
            errors.append("max_workers must be >= 1")
        if self.refresh_interval < 1:
            errors.append("refresh_interval must be >= 1")
        if self.enable_upload and not self.dropbox_token:
            errors.append("Dropbox token required when upload is enabled")
            
        return errors


class JGTServiceManager:
    """Main service manager for JGT Data Refresh Service"""
    
    def __init__(self, config: JGTServiceConfig):
        self.config = config
        self.running = False
        self.scheduler = None
        self.processor = None
        self.uploader = None
        self.web_server = None
        self.shutdown_event = threading.Event()
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("JGT Service Manager initialized")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, initiating shutdown...")
        self.stop()
    
    def start(self):
        """Start the service based on configuration"""
        logger.info("Starting JGT Service...")
        
        # Validate configuration
        errors = self.config.validate()
        if errors:
            for error in errors:
                logger.error(f"Configuration error: {error}")
            raise ValueError(f"Configuration validation failed: {errors}")
        
        self.running = True
        
        try:
            # Initialize components
            self._initialize_components()
            
            if self.config.refresh_once:
                # One-time refresh mode
                self._run_one_time_refresh()
            elif self.config.web_mode:
                # Web server mode
                self._run_web_server()
            elif self.config.daemon_mode:
                # Daemon mode with scheduler
                self._run_daemon()
            else:
                # Default: run once then exit
                self._run_one_time_refresh()
                
        except Exception as e:
            logger.error(f"Service startup failed: {e}")
            self.stop()
            raise
    
    def stop(self):
        """Stop the service gracefully"""
        if not self.running:
            return
            
        logger.info("Stopping JGT Service...")
        self.running = False
        self.shutdown_event.set()
        
        # Stop components
        if self.scheduler:
            self.scheduler.stop()
        if self.processor:
            self.processor.shutdown()
        
        logger.info("JGT Service stopped")
    
    def _initialize_components(self):
        """Initialize service components"""
        from .scheduler import JGTScheduler
        from .processor import ParallelProcessor
        
        # Initialize processor (always needed)
        self.processor = ParallelProcessor(
            max_workers=self.config.max_workers,
            config=self.config
        )
        logger.info(f"Initialized processor with {self.config.max_workers} workers")
        
        # Initialize uploader if enabled and token available
        if self.config.enable_upload and self.config.dropbox_token:
            try:
                from .uploader import CloudUploader
                self.uploader = CloudUploader(
                    token=self.config.dropbox_token,
                    config=self.config
                )
                logger.info("Initialized cloud uploader")
            except ImportError as e:
                logger.warning(f"Could not initialize uploader: {e}")
                logger.warning("Install dropbox package: pip install dropbox")
                self.uploader = None
        else:
            if not self.config.enable_upload:
                logger.info("Upload disabled in configuration")
            else:
                logger.warning("Upload enabled but no Dropbox token found")
            self.uploader = None
        
        # Initialize scheduler for daemon mode
        if self.config.daemon_mode:
            self.scheduler = JGTScheduler(
                config=self.config,
                processor=self.processor,
                uploader=self.uploader
            )
            logger.info("Initialized scheduler for daemon mode")
    
    def _run_one_time_refresh(self):
        """Run one-time data refresh"""
        logger.info("Running one-time data refresh...")
        
        # Process all configured instruments/timeframes
        results = self.processor.process_all_instruments_timeframes()
        
        successful = sum(1 for r in results if r.success)
        logger.info(f"Data processing completed: {successful}/{len(results)} successful")
        
        # Upload if configured and uploader available
        if self.uploader and results:
            upload_results = self.uploader.upload_processing_results(results)
            upload_successful = sum(1 for r in upload_results if r.success)
            logger.info(f"Upload completed: {upload_successful}/{len(upload_results)} files uploaded")
        
        logger.info("One-time refresh completed")
    
    def _run_daemon(self):
        """Run in daemon mode with scheduler"""
        logger.info("Starting daemon mode...")
        
        # Start the scheduler
        if self.scheduler:
            self.scheduler.start()
            logger.info("Scheduler started")
        else:
            logger.error("No scheduler initialized for daemon mode")
            return
        
        # Wait for shutdown signal
        while self.running and not self.shutdown_event.is_set():
            self.shutdown_event.wait(timeout=1.0)
        
        # Stop the scheduler
        if self.scheduler:
            self.scheduler.stop()
        
        logger.info("Daemon mode shutting down...")
    
    def _run_web_server(self):
        """Run web server mode"""
        logger.info(f"Starting web server on port {self.config.web_port}...")
        
        # Will be implemented in later phase
        logger.info("Web server mode not yet implemented")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current service status"""
        status = {
            "running": self.running,
            "config": {
                "instruments": self.config.instruments,
                "timeframes": self.config.timeframes,
                "max_workers": self.config.max_workers,
                "enable_upload": self.config.enable_upload
            }
        }
        
        return status

