"""
JGT Scheduler Module

Provides timeframe-based scheduling capabilities for the JGT data refresh service.
Based on patterns from jgtutils.timeframe_scheduler but adapted for service use.
"""

import sys
import os
import time
import threading
import logging
from datetime import datetime
from typing import Dict, List, Callable, Optional

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

logger = logging.getLogger(__name__)

class JGTScheduler:
    """Timeframe-based scheduler for JGT data refresh service"""
    
    def __init__(self, config, processor=None, uploader=None):
        self.config = config
        self.processor = processor
        self.uploader = uploader
        self.running = False
        self.scheduler_thread = None
        self.last_refresh_times = {}
        
        logger.info("JGT Scheduler initialized")
    
    def start(self):
        """Start the scheduler in a separate thread"""
        if self.running:
            logger.warning("Scheduler already running")
            return
        
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logger.info("JGT Scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        if not self.running:
            return
        
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5.0)
        
        logger.info("JGT Scheduler stopped")
    
    def _run_scheduler(self):
        """Main scheduler loop"""
        logger.info("Scheduler loop started")
        
        while self.running:
            try:
                current_time = datetime.now()
                
                # Check each configured timeframe
                for timeframe in self.config.timeframes:
                    if self._should_refresh(timeframe, current_time):
                        self._trigger_refresh(timeframe)
                        self.last_refresh_times[timeframe] = current_time
                
                # Sleep for 1 second before next check
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                if not self.config.continue_on_error:
                    break
                time.sleep(5)  # Wait before retrying
        
        logger.info("Scheduler loop ended")
    
    def _should_refresh(self, timeframe: str, current_time: datetime) -> bool:
        """Check if timeframe should be refreshed at current time"""
        # This is a simplified version - would need full timeframe logic
        # from jgtutils.timeframe_scheduler
        
        current_minute = current_time.minute
        current_hour = current_time.hour
        
        # Basic timeframe checking (simplified)
        if timeframe == "m5" and current_minute % 5 == 0:
            return True
        elif timeframe == "m15" and current_minute % 15 == 0:
            return True
        elif timeframe == "H1" and current_minute == 0:
            return True
        elif timeframe == "H4" and current_minute == 0 and current_hour % 4 == 0:
            return True
        
        return False
    
    def _trigger_refresh(self, timeframe: str):
        """Trigger data refresh for specific timeframe"""
        logger.info(f"Triggering refresh for timeframe: {timeframe}")
        
        if self.processor:
            # Process all instruments for this timeframe
            try:
                results = self.processor.process_instruments_timeframes(
                    self.config.instruments, 
                    [timeframe]
                )
                
                # Upload if configured
                if self.uploader and results:
                    self.uploader.upload_results(results)
                    
            except Exception as e:
                logger.error(f"Refresh failed for {timeframe}: {e}")
    
    def get_status(self) -> Dict:
        """Get scheduler status"""
        return {
            'running': self.running,
            'last_refresh_times': self.last_refresh_times,
            'configured_timeframes': self.config.timeframes
        } 