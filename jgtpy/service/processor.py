"""
JGT Parallel Processor Module

Provides parallel processing capabilities for data refresh operations.
Integrates with existing JGTCDSSvc, JGTIDSSvc, and JGTPDSPSvc.
"""

import sys
import os
import logging
import concurrent.futures
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import from parent jgtpy package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logger = logging.getLogger(__name__)

@dataclass
class ProcessingResult:
    """Result of a single processing operation"""
    instrument: str
    timeframe: str
    success: bool
    file_path: Optional[str] = None
    error: Optional[str] = None
    processing_time: float = 0.0

class ParallelProcessor:
    """Parallel processor for JGT data operations"""
    
    def __init__(self, max_workers: int = 4, config=None):
        self.max_workers = max_workers
        self.config = config
        self.executor = None
        
        logger.info(f"Parallel Processor initialized with {max_workers} workers")
    
    def process_all_instruments_timeframes(self) -> List[ProcessingResult]:
        """Process all configured instruments and timeframes"""
        return self.process_instruments_timeframes(
            self.config.instruments,
            self.config.timeframes
        )
    
    def process_instruments_timeframes(self, instruments: List[str], 
                                     timeframes: List[str]) -> List[ProcessingResult]:
        """Process specific instruments and timeframes in parallel"""
        logger.info(f"Processing {len(instruments)} instruments x {len(timeframes)} timeframes")
        
        # Create tasks for all instrument/timeframe combinations
        tasks = []
        for instrument in instruments:
            for timeframe in timeframes:
                tasks.append((instrument, timeframe))
        
        results = []
        
        # Process tasks in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            self.executor = executor
            
            # Submit all tasks
            future_to_task = {
                executor.submit(self._process_single, instrument, timeframe): (instrument, timeframe)
                for instrument, timeframe in tasks
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_task):
                instrument, timeframe = future_to_task[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    if result.success:
                        logger.info(f"✓ {instrument}/{timeframe} completed in {result.processing_time:.2f}s")
                    else:
                        logger.error(f"✗ {instrument}/{timeframe} failed: {result.error}")
                        
                except Exception as exc:
                    logger.error(f"✗ {instrument}/{timeframe} generated exception: {exc}")
                    results.append(ProcessingResult(
                        instrument=instrument,
                        timeframe=timeframe,
                        success=False,
                        error=str(exc)
                    ))
        
        self.executor = None
        
        # Log summary
        successful = sum(1 for r in results if r.success)
        logger.info(f"Processing completed: {successful}/{len(results)} successful")
        
        return results
    
    def _process_single(self, instrument: str, timeframe: str) -> ProcessingResult:
        """Process a single instrument/timeframe combination"""
        import time
        start_time = time.time()
        
        try:
            logger.debug(f"Processing {instrument}/{timeframe}")
            
            # Import and use actual JGTCDSSvc
            from JGTCDSSvc import get
            
            # Process using real CDS service
            cdf = get(
                instrument=instrument,
                timeframe=timeframe,
                use_fresh=self.config.use_fresh,
                use_full=self.config.use_full,
                quiet=self.config.quiet,
                quotescount=-1  # Use default quote count
            )
            
            processing_time = time.time() - start_time
            
            if cdf is not None and len(cdf) > 0:
                # Generate expected file path based on config
                data_path = self.config.data_full_path if self.config.use_full else self.config.data_path
                file_path = f"{data_path}/cds/{instrument}_{timeframe}.csv"
                
                logger.debug(f"✓ {instrument}/{timeframe} processed: {len(cdf)} rows")
                
                return ProcessingResult(
                    instrument=instrument,
                    timeframe=timeframe,
                    success=True,
                    file_path=file_path,
                    processing_time=processing_time
                )
            else:
                return ProcessingResult(
                    instrument=instrument,
                    timeframe=timeframe,
                    success=False,
                    error="CDS processing returned empty result",
                    processing_time=processing_time
                )
            
        except ImportError as e:
            processing_time = time.time() - start_time
            error_msg = f"Could not import JGTCDSSvc: {e}"
            logger.error(f"Failed to process {instrument}/{timeframe}: {error_msg}")
            
            return ProcessingResult(
                instrument=instrument,
                timeframe=timeframe,
                success=False,
                error=error_msg,
                processing_time=processing_time
            )
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = f"Processing error: {e}"
            logger.error(f"Failed to process {instrument}/{timeframe}: {error_msg}")
            
            return ProcessingResult(
                instrument=instrument,
                timeframe=timeframe,
                success=False,
                error=error_msg,
                processing_time=processing_time
            )
    
    def shutdown(self):
        """Shutdown the processor"""
        if self.executor:
            self.executor.shutdown(wait=True)
        logger.info("Parallel Processor shutdown")
    
    def get_status(self) -> Dict[str, Any]:
        """Get processor status"""
        return {
            'max_workers': self.max_workers,
            'active': self.executor is not None
        } 