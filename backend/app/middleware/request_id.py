"""Request ID middleware for structured log correlation.

Attaches a unique ``X-Request-ID`` to every request. If the client sends one,
it is preserved. Otherwise a new UUID4 is generated. The ID is:
  - Stored on ``request.state.request_id`` for handler access.
  - Returned in every response as ``X-Request-ID`` header.
  - Included in structured log output via a logging filter.

Usage in main.py:
    from app.middleware.request_id import RequestIDMiddleware
    app.add_middleware(RequestIDMiddleware)
"""

from __future__ import annotations

import logging
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)

HEADER_NAME = "X-Request-ID"
MAX_HEADER_LENGTH = 64  # Reject suspiciously long IDs


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Attach a stable request ID to every request/response cycle."""

    async def dispatch(self, request: Request, call_next) -> Response:  # type: ignore[override]
        # Use client-supplied ID if present and safe; otherwise generate one
        incoming = request.headers.get(HEADER_NAME, "")
        if incoming and len(incoming) <= MAX_HEADER_LENGTH and incoming.isascii():
            request_id = incoming
        else:
            request_id = f"req_{uuid.uuid4().hex[:12]}"

        # Make available to handlers and error responses
        request.state.request_id = request_id

        # Inject into log context for this request
        _log_filter = _RequestIDFilter(request_id)
        root_logger = logging.getLogger()
        root_logger.addFilter(_log_filter)

        try:
            response: Response = await call_next(request)
        finally:
            root_logger.removeFilter(_log_filter)

        response.headers[HEADER_NAME] = request_id
        return response


class _RequestIDFilter(logging.Filter):
    """Logging filter that injects request_id into all log records."""

    def __init__(self, request_id: str) -> None:
        super().__init__()
        self.request_id = request_id

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = self.request_id  # type: ignore[attr-defined]
        return True
