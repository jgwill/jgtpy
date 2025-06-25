"""
JGT Data Refresh Service - FastAPI Web Service

Provides RESTful API endpoints for data access, service management, and monitoring.
Implements modern async web framework with OpenAPI documentation.
"""
from __future__ import annotations

import logging
import os
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from fastapi.security import HTTPAuthorizationCredentials

try:
    from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
    from fastapi.responses import JSONResponse, FileResponse
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    import uvicorn
    _has_fastapi = True
except ImportError:
    _has_fastapi = False
    FastAPI = None
    uvicorn = None

from .base import JGTServiceConfig, JGTServiceManager
from .processor import ParallelProcessor

logger = logging.getLogger(__name__)

class JGTServiceAPI:
    """FastAPI web service for JGT Data Refresh Service"""
    
    def __init__(self, config: JGTServiceConfig, service_manager: JGTServiceManager):
        if not _has_fastapi:
            raise ImportError("FastAPI dependencies not available. Install with: pip install jgtpy[serve]")
        
        self.config = config
        self.service_manager = service_manager
        self.app = FastAPI(
            title="JGT Data Refresh Service API",
            description="RESTful API for financial market data processing and distribution",
            version="0.6.0",
            docs_url="/docs",
            redoc_url="/redoc"
        )
        
        # Security (optional)
        self.security = HTTPBearer(auto_error=False) if os.getenv("JGTPY_API_KEY") else None
        
        # Setup middleware
        self._setup_middleware()
        
        # Setup routes
        self._setup_routes()
        
        logger.info("JGT Service API initialized")
    
    def _setup_middleware(self):
        """Setup FastAPI middleware"""
        
        # CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure appropriately for production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def _verify_api_key(self, credentials: Optional["HTTPAuthorizationCredentials"] = None):
        """Verify API key if authentication is enabled"""
        api_key = os.getenv("JGTPY_API_KEY")
        if not api_key:
            return True  # No authentication required
        
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        if credentials.credentials != api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
        
        return True
    
    def _setup_routes(self):
        """Setup API routes"""
        
        # Health and status endpoints
        @self.app.get("/api/v1/health")
        async def health_check():
            """Health check endpoint"""
            return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
        
        @self.app.get("/api/v1/status")
        async def get_status(authenticated: bool = Depends(self._verify_api_key)):
            """Get service status and configuration"""
            try:
                status = self.service_manager.get_status()
                return JSONResponse(content=status)
            except Exception as e:
                logger.error(f"Status request failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Data access endpoints
        @self.app.get("/api/v1/instruments")
        async def list_instruments(authenticated: bool = Depends(self._verify_api_key)):
            """List available instruments"""
            return {"instruments": self.config.instruments}
        
        @self.app.get("/api/v1/timeframes")
        async def list_timeframes(authenticated: bool = Depends(self._verify_api_key)):
            """List available timeframes"""
            return {"timeframes": self.config.timeframes}
        
        @self.app.get("/api/v1/data/{instrument}/{timeframe}")
        async def get_data(
            instrument: str, 
            timeframe: str,
            format: str = "json",
            limit: Optional[int] = None,
            authenticated: bool = Depends(self._verify_api_key)
        ):
            """Retrieve processed CDS data for instrument/timeframe"""
            try:
                # Validate parameters
                if instrument not in self.config.instruments:
                    raise HTTPException(status_code=404, detail=f"Instrument {instrument} not configured")
                
                if timeframe not in self.config.timeframes:
                    raise HTTPException(status_code=404, detail=f"Timeframe {timeframe} not configured")
                
                # Find data file
                data_path = Path(self.config.data_path) / "cds" / instrument.replace("/", "") / f"{timeframe}.cds"
                
                if not data_path.exists():
                    raise HTTPException(status_code=404, detail=f"Data not found for {instrument} {timeframe}")
                
                if format.lower() == "csv":
                    # Return CSV file directly
                    return FileResponse(
                        path=str(data_path),
                        media_type="text/csv",
                        filename=f"{instrument.replace('/', '')}_{timeframe}.csv"
                    )
                
                # Read and return JSON data
                import pandas as pd
                try:
                    df = pd.read_csv(data_path)
                    if limit:
                        df = df.tail(limit)
                    
                    # Convert to JSON
                    data = {
                        "instrument": instrument,
                        "timeframe": timeframe,
                        "records": len(df),
                        "last_updated": datetime.fromtimestamp(data_path.stat().st_mtime).isoformat(),
                        "data": df.to_dict(orient="records")
                    }
                    
                    return JSONResponse(content=data)
                    
                except Exception as e:
                    logger.error(f"Failed to read data file {data_path}: {e}")
                    raise HTTPException(status_code=500, detail=f"Failed to read data: {e}")
                
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Data request failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/v1/data/{instrument}/{timeframe}/latest")
        async def get_latest_data(
            instrument: str, 
            timeframe: str,
            authenticated: bool = Depends(self._verify_api_key)
        ):
            """Get latest data point for instrument/timeframe"""
            try:
                # Validate parameters
                if instrument not in self.config.instruments:
                    raise HTTPException(status_code=404, detail=f"Instrument {instrument} not configured")
                
                if timeframe not in self.config.timeframes:
                    raise HTTPException(status_code=404, detail=f"Timeframe {timeframe} not configured")
                
                # Find data file
                data_path = Path(self.config.data_path) / "cds" / instrument.replace("/", "") / f"{timeframe}.cds"
                
                if not data_path.exists():
                    raise HTTPException(status_code=404, detail=f"Data not found for {instrument} {timeframe}")
                
                # Read latest record
                import pandas as pd
                try:
                    df = pd.read_csv(data_path)
                    latest = df.tail(1).iloc[0].to_dict()
                    
                    return JSONResponse(content={
                        "instrument": instrument,
                        "timeframe": timeframe,
                        "last_updated": datetime.fromtimestamp(data_path.stat().st_mtime).isoformat(),
                        "latest": latest
                    })
                    
                except Exception as e:
                    logger.error(f"Failed to read data file {data_path}: {e}")
                    raise HTTPException(status_code=500, detail=f"Failed to read data: {e}")
                
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Latest data request failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Service management endpoints
        @self.app.post("/api/v1/refresh")
        async def trigger_refresh(
            background_tasks: BackgroundTasks,
            instruments: Optional[List[str]] = None,
            timeframes: Optional[List[str]] = None,
            authenticated: bool = Depends(self._verify_api_key)
        ):
            """Trigger manual data refresh"""
            try:
                # Use provided instruments/timeframes or defaults
                target_instruments = instruments or self.config.instruments
                target_timeframes = timeframes or self.config.timeframes
                
                # Validate parameters
                for instrument in target_instruments:
                    if instrument not in self.config.instruments:
                        raise HTTPException(status_code=400, detail=f"Instrument {instrument} not configured")
                
                for timeframe in target_timeframes:
                    if timeframe not in self.config.timeframes:
                        raise HTTPException(status_code=400, detail=f"Timeframe {timeframe} not configured")
                
                # Start background refresh
                async def run_refresh():
                    try:
                        processor = ParallelProcessor(self.config)
                        await asyncio.get_event_loop().run_in_executor(
                            None, 
                            processor.process_all,
                            target_instruments,
                            target_timeframes
                        )
                        logger.info(f"Manual refresh completed for {target_instruments} {target_timeframes}")
                    except Exception as e:
                        logger.error(f"Manual refresh failed: {e}")
                
                background_tasks.add_task(run_refresh)
                
                return JSONResponse(content={
                    "status": "refresh_started",
                    "instruments": target_instruments,
                    "timeframes": target_timeframes,
                    "timestamp": datetime.utcnow().isoformat()
                })
                
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Refresh trigger failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Monitoring endpoints
        @self.app.get("/api/v1/config")
        async def get_config(authenticated: bool = Depends(self._verify_api_key)):
            """Get current configuration (sanitized)"""
            try:
                config_dict = {
                    "instruments": self.config.instruments,
                    "timeframes": self.config.timeframes,
                    "max_workers": self.config.max_workers,
                    "data_path": self.config.data_path,
                    "enable_upload": self.config.enable_upload,
                    "use_fresh": self.config.use_fresh,
                    "use_full": self.config.use_full,
                    "refresh_interval": self.config.refresh_interval
                }
                return JSONResponse(content=config_dict)
                
            except Exception as e:
                logger.error(f"Config request failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/v1/metrics")
        async def get_metrics(authenticated: bool = Depends(self._verify_api_key)):
            """Get processing metrics and statistics"""
            try:
                # Basic metrics - can be enhanced with actual processing stats
                metrics = {
                    "service_uptime": "N/A",  # TODO: Calculate actual uptime
                    "total_instruments": len(self.config.instruments),
                    "total_timeframes": len(self.config.timeframes),
                    "configured_workers": self.config.max_workers,
                    "data_files": self._count_data_files(),
                    "last_refresh": "N/A",  # TODO: Track last refresh time
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                return JSONResponse(content=metrics)
                
            except Exception as e:
                logger.error(f"Metrics request failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/v1/upload/status")
        async def get_upload_status(authenticated: bool = Depends(self._verify_api_key)):
            """Get upload status and metrics"""
            try:
                status_data = {
                    "upload_enabled": self.config.enable_upload,
                    "dropbox_configured": bool(self.config.dropbox_token),
                    "upload_path_current": self.config.upload_path_current,
                    "upload_path_full": self.config.upload_path_full,
                    "last_upload": "N/A",  # TODO: Track last upload time
                    "upload_errors": "N/A",  # TODO: Track upload errors
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                return JSONResponse(content=status_data)
                
            except Exception as e:
                logger.error(f"Upload status request failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
    
    def _count_data_files(self) -> Dict[str, int]:
        """Count available data files"""
        try:
            data_path = Path(self.config.data_path)
            counts = {
                "cds_files": 0,
                "instruments_with_data": 0,
                "total_size_mb": 0
            }
            
            if data_path.exists():
                cds_path = data_path / "cds"
                if cds_path.exists():
                    instruments_with_data = set()
                    total_size = 0
                    
                    for file_path in cds_path.rglob("*.cds"):
                        counts["cds_files"] += 1
                        instruments_with_data.add(file_path.parent.name)
                        total_size += file_path.stat().st_size
                    
                    counts["instruments_with_data"] = len(instruments_with_data)
                    counts["total_size_mb"] = round(total_size / (1024 * 1024), 2)
            
            return counts
            
        except Exception as e:
            logger.error(f"Failed to count data files: {e}")
            return {"error": str(e)}
    
    async def start_server(self):
        """Start the FastAPI server"""
        if not _has_fastapi:
            raise ImportError("FastAPI dependencies not available. Install with: pip install jgtpy[serve]")
        
        logger.info(f"Starting JGT Service API server on port {self.config.web_port}")
        
        config = uvicorn.Config(
            self.app,
            host="0.0.0.0",
            port=self.config.web_port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()


def create_api_app(config: JGTServiceConfig, service_manager: JGTServiceManager) -> FastAPI:
    """Factory function to create FastAPI app"""
    api = JGTServiceAPI(config, service_manager)
    return api.app 