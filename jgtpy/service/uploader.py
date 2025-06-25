"""
JGT Cloud Uploader Module

Modernizes Dropbox integration for automated data distribution.
Based on JGTCloudFS.py but updated to use current dropbox package.
"""

import sys
import os
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import time
from dataclasses import dataclass

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import dropbox if available
try:
    import dropbox
    from dropbox.exceptions import AuthError, ApiError
    _has_dropbox = True
except ImportError:
    _has_dropbox = False

logger = logging.getLogger(__name__)

@dataclass
class UploadResult:
    """Result of a single upload operation"""
    local_path: str
    remote_path: str
    success: bool
    file_size: int = 0
    upload_time: float = 0.0
    error: Optional[str] = None

class CloudUploader:
    """Modern Dropbox uploader for JGT data distribution"""
    
    def __init__(self, token: str = None, config=None):
        if not _has_dropbox:
            raise ImportError("dropbox package not available. Install with: pip install dropbox")
        
        self.token = token
        self.config = config
        self.dbx = None
        self.connect()
        
        logger.info("Cloud Uploader initialized")
    
    def connect(self):
        """Connect to Dropbox API (supports short-lived tokens with refresh)."""
        try:
            if self.config and self.config.dropbox_refresh_token and self.config.dropbox_app_key and self.config.dropbox_app_secret:
                logger.debug("Connecting to Dropbox using refresh token flow")
                self.dbx = dropbox.Dropbox(
                    oauth2_refresh_token=self.config.dropbox_refresh_token,
                    app_key=self.config.dropbox_app_key,
                    app_secret=self.config.dropbox_app_secret,
                )
            elif self.token:
                logger.debug("Connecting to Dropbox using access token")
                self.dbx = dropbox.Dropbox(self.token)
            else:
                raise AuthError("", "No Dropbox credentials provided")

            # Test connection
            self.dbx.users_get_current_account()
            logger.info("Connected to Dropbox successfully")
        except AuthError as e:
            logger.error(f"Dropbox authentication failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to connect to Dropbox: {e}")
            raise
    
    def upload_file(self, local_path: str, remote_path: str) -> UploadResult:
        """Upload a single file to Dropbox"""
        start_time = time.time()
        local_path_obj = Path(local_path)
        
        if not local_path_obj.exists():
            return UploadResult(
                local_path=local_path,
                remote_path=remote_path,
                success=False,
                error="Local file does not exist"
            )
        
        file_size = local_path_obj.stat().st_size
        
        # Try Python dropbox library first
        try:
            # Ensure remote path starts with /
            if not remote_path.startswith('/'):
                remote_path = '/' + remote_path
            
            logger.debug(f"Uploading {local_path} -> {remote_path}")
            
            with open(local_path, 'rb') as f:
                if file_size <= 150 * 1024 * 1024:  # 150MB limit for simple upload
                    self.dbx.files_upload(f.read(), remote_path, mode=dropbox.files.WriteMode.overwrite)
                else:
                    # Use upload session for large files
                    self._upload_large_file(f, remote_path, file_size)
            
            upload_time = time.time() - start_time
            logger.info(f"✓ Uploaded {local_path_obj.name} ({file_size} bytes) in {upload_time:.2f}s")
            
            return UploadResult(
                local_path=local_path,
                remote_path=remote_path,
                success=True,
                file_size=file_size,
                upload_time=upload_time
            )
            
        except Exception as e:
            logger.warning(f"Python dropbox upload failed: {e}")
            logger.info("Falling back to droxul command...")
            
            # Fallback to droxul command
            return self._upload_with_droxul(local_path, remote_path, file_size, start_time)
    
    def _upload_with_droxul(self, local_path: str, remote_path: str, file_size: int, start_time: float) -> UploadResult:
        """Upload using droxul command as fallback"""
        try:
            import subprocess
            
            # droxul upload $path_of_instrument_timeframe_csv /dist/data/current/
            remote_dir = str(Path(remote_path).parent)
            
            cmd = ["droxul", "upload", local_path, remote_dir]
            logger.debug(f"Running: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            upload_time = time.time() - start_time
            
            if result.returncode == 0:
                logger.info(f"✓ Uploaded via droxul: {Path(local_path).name} ({file_size} bytes) in {upload_time:.2f}s")
                return UploadResult(
                    local_path=local_path,
                    remote_path=remote_path,
                    success=True,
                    file_size=file_size,
                    upload_time=upload_time
                )
            else:
                error_msg = f"droxul command failed: {result.stderr}"
                logger.error(f"✗ droxul upload failed: {error_msg}")
                return UploadResult(
                    local_path=local_path,
                    remote_path=remote_path,
                    success=False,
                    file_size=file_size,
                    upload_time=upload_time,
                    error=error_msg
                )
                
        except Exception as e:
            upload_time = time.time() - start_time
            error_msg = f"droxul fallback failed: {e}"
            logger.error(f"✗ All upload methods failed: {error_msg}")
            return UploadResult(
                local_path=local_path,
                remote_path=remote_path,
                success=False,
                file_size=file_size,
                upload_time=upload_time,
                error=error_msg
            )
    
    def _upload_large_file(self, file_obj, remote_path: str, file_size: int):
        """Upload large files using upload session"""
        CHUNK_SIZE = 4 * 1024 * 1024  # 4MB chunks
        
        session_start_result = self.dbx.files_upload_session_start(file_obj.read(CHUNK_SIZE))
        cursor = dropbox.files.UploadSessionCursor(
            session_id=session_start_result.session_id,
            offset=file_obj.tell()
        )
        
        # Upload remaining chunks
        while file_obj.tell() < file_size:
            chunk = file_obj.read(CHUNK_SIZE)
            if len(chunk) <= CHUNK_SIZE:
                # Last chunk
                commit = dropbox.files.CommitInfo(path=remote_path, mode=dropbox.files.WriteMode.overwrite)
                self.dbx.files_upload_session_finish(chunk, cursor, commit)
                break
            else:
                self.dbx.files_upload_session_append_v2(chunk, cursor)
                cursor.offset = file_obj.tell()
    
    def upload_batch(self, file_mappings: List[Tuple[str, str]]) -> List[UploadResult]:
        """Upload multiple files in sequence"""
        results = []
        
        logger.info(f"Starting batch upload of {len(file_mappings)} files")
        
        for local_path, remote_path in file_mappings:
            result = self.upload_file(local_path, remote_path)
            results.append(result)
            
            # Add small delay between uploads to be nice to the API
            time.sleep(0.1)
        
        successful = sum(1 for r in results if r.success)
        total_size = sum(r.file_size for r in results if r.success)
        total_time = sum(r.upload_time for r in results)
        
        logger.info(f"Batch upload completed: {successful}/{len(results)} successful, "
                   f"{total_size} bytes in {total_time:.2f}s")
        
        return results
    
    def upload_processing_results(self, processing_results) -> List[UploadResult]:
        """Upload results from data processing operations"""
        if not processing_results:
            return []
        
        file_mappings = []
        
        for result in processing_results:
            if result.success and result.file_path:
                local_path = result.file_path
                
                # Check if file actually exists (since CDS service writes files)
                if not Path(local_path).exists():
                    logger.warning(f"File does not exist: {local_path}")
                    continue
                
                # Determine remote path based on data type and config  
                # Use /dist/data/current/ pattern as per user's droxul usage
                if self.config.use_full:
                    remote_dir = "/dist/data/full/"
                else:
                    remote_dir = "/dist/data/current/"
                
                # Create remote path
                filename = Path(local_path).name
                remote_path = f"{remote_dir}{filename}"
                
                file_mappings.append((local_path, remote_path))
        
        if file_mappings:
            return self.upload_batch(file_mappings)
        else:
            logger.warning("No files to upload from processing results")
            return []
    
    def verify_upload(self, remote_path: str) -> bool:
        """Verify that a file exists on Dropbox"""
        try:
            if not remote_path.startswith('/'):
                remote_path = '/' + remote_path
            
            self.dbx.files_get_metadata(remote_path)
            return True
        except ApiError:
            return False
        except Exception as e:
            logger.error(f"Error verifying upload {remote_path}: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get uploader status"""
        status = {
            'connected': self.dbx is not None,
            'token_set': bool(self.token)
        }
        
        if self.dbx:
            try:
                account = self.dbx.users_get_current_account()
                status['account_name'] = account.name.display_name
                status['account_email'] = account.email
            except Exception as e:
                status['connection_error'] = str(e)
        
        return status 