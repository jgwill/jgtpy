# JGTServiceAPI Specification

The FastAPI web service exposes endpoints for data access and service management for JGT Data Refresh.

## Authentication Logic
- Uses `HTTPBearer` when the environment variable `JGTPY_API_KEY` is present.
- `_verify_api_key(credentials)` checks the bearer token and raises `HTTPException` on failure.
- When no API key is configured, all endpoints allow anonymous access.

## Implementation Notes
- `from __future__ import annotations` is imported to allow forward references in type hints.
- The service manager provides status and metrics; data files are served from the configured `data_path`.

