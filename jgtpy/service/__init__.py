"""
JGT Data Refresh Service Module

This module provides automated data refresh services for jgtpy package with:
- Timeframe-based scheduling
- Parallel processing capabilities  
- Cloud distribution integration
- Web API endpoints

Main Components:
- JGTScheduler: Timeframe-based task scheduling
- JGTServiceManager: Main service orchestration
- ParallelProcessor: Multi-threaded data processing
- CloudUploader: Dropbox integration for data distribution
- ServiceAPI: Web API endpoints for data access
"""

from .base import JGTServiceManager, JGTServiceConfig
from .scheduler import JGTScheduler
from .processor import ParallelProcessor

# Optional imports that might not be available
try:
    from .uploader import CloudUploader
    _has_uploader = True
except ImportError:
    CloudUploader = None
    _has_uploader = False

try:
    from .api import JGTServiceAPI
    _has_api = True
except ImportError:
    JGTServiceAPI = None
    _has_api = False

__all__ = [
    'JGTServiceManager',
    'JGTServiceConfig', 
    'JGTScheduler',
    'ParallelProcessor',
]

if _has_uploader:
    __all__.append('CloudUploader')

if _has_api:
    __all__.append('JGTServiceAPI')

__version__ = "0.1.0" 
