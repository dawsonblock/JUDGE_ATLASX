"""Legacy admin ingestion router exposure.

This module intentionally isolates legacy/U.S.-focused ingestion endpoints from
core Canada-first admin ingestion routes.
"""

from app.api.routes.admin_ingest import legacy_router as router

__all__ = ["router"]
