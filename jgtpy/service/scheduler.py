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
        # Use the real timeframe scheduling logic from jgtutils
        try:
            from jgtutils.timeframe_scheduler import get_times_by_timeframe_str, get_current_time
            
            # Get valid times for this timeframe
            valid_times = get_times_by_timeframe_str(timeframe)
            if not valid_times:
                return False
            
            # Get current time in the format expected by timeframe scheduler
            current_time_str = get_current_time(timeframe)
            
            # Check if current time matches any valid time
            is_valid_time = current_time_str in valid_times
            
            # Only trigger if we haven't processed this timeframe in the last minute
            # to avoid duplicate processing
            last_refresh = self.last_refresh_times.get(timeframe)
            if last_refresh and (current_time - last_refresh).total_seconds() < 60:
                return False
            
            return is_valid_time
            
        except ImportError:
            logger.warning("Could not import jgtutils.timeframe_scheduler, using fallback logic")
            # Fallback to simplified logic
            current_minute = current_time.minute
            current_hour = current_time.hour
            
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
                    upload_results = self.uploader.upload_processing_results(results)
                    upload_successful = sum(1 for r in upload_results if r.success)
                    logger.info(f"Upload completed: {upload_successful}/{len(upload_results)} files uploaded")
                    
            except Exception as e:
                logger.error(f"Refresh failed for {timeframe}: {e}")
    
    def get_status(self) -> Dict:
        """Get scheduler status"""
        return {
            'running': self.running,
            'last_refresh_times': self.last_refresh_times,
            'configured_timeframes': self.config.timeframes
        } 