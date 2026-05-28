"""Structured error types and response shapes for JUDGE_ATLASX.

All API error responses use the ``ErrorResponse`` Pydantic model so clients
receive a consistent envelope regardless of which route raised the error.

Error envelope
--------------
{
    "error": {
        "code": "VALIDATION_ERROR",       # Machine-readable error code
        "message": "...",                  # Human-readable summary
        "detail": [...],                   # Optional structured detail
        "request_id": "req_abc123"         # Unique ID for log correlation
    }
}

Usage in route handlers
-----------------------
    from app.core.errors import AppError, ErrorCode
    raise AppError(ErrorCode.SOURCE_NOT_FOUND, f"Source '{key}' not found")

FastAPI exception handlers
--------------------------
Register them in main.py:
    from app.core.errors import register_exception_handlers
    register_exception_handlers(app)
"""

from __future__ import annotations

import logging
from enum import Enum
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Error codes
# ---------------------------------------------------------------------------

class ErrorCode(str, Enum):
    # Generic
    INTERNAL_ERROR = "INTERNAL_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    CONFLICT = "CONFLICT"
    RATE_LIMITED = "RATE_LIMITED"

    # Ingestion
    SOURCE_NOT_FOUND = "SOURCE_NOT_FOUND"
    SOURCE_DISABLED = "SOURCE_DISABLED"
    PARSER_VERSION_MISMATCH = "PARSER_VERSION_MISMATCH"
    INGESTION_QUARANTINED = "INGESTION_QUARANTINED"
    DRY_RUN_FAILED = "DRY_RUN_FAILED"

    # Review
    REVIEW_STATE_INVALID = "REVIEW_STATE_INVALID"
    REVIEW_CONFLICT = "REVIEW_CONFLICT"
    HIGH_RISK_APPROVAL_REQUIRED = "HIGH_RISK_APPROVAL_REQUIRED"

    # Public platform
    RECORD_NOT_PUBLISHED = "RECORD_NOT_PUBLISHED"
    RECORD_SUPPRESSED = "RECORD_SUPPRESSED"
    RECORD_STALE = "RECORD_STALE"
    PUBLICATION_BLOCKED_BY_CONTRADICTION = "PUBLICATION_BLOCKED_BY_CONTRADICTION"

    # Security
    NETWORK_POLICY_VIOLATION = "NETWORK_POLICY_VIOLATION"
    IMPORT_AUTHORITY_DENIED = "IMPORT_AUTHORITY_DENIED"


# ---------------------------------------------------------------------------
# Response shape
# ---------------------------------------------------------------------------

class ErrorDetail(BaseModel):
    """Optional structured detail attached to an error."""
    field: str | None = None
    message: str
    value: Any | None = None


class ErrorEnvelope(BaseModel):
    """Inner error object."""
    code: str
    message: str
    detail: list[ErrorDetail] | None = None
    request_id: str | None = None


class ErrorResponse(BaseModel):
    """Top-level error response envelope."""
    error: ErrorEnvelope


# ---------------------------------------------------------------------------
# Application exception
# ---------------------------------------------------------------------------

class AppError(Exception):
    """Raise this from any route or service to produce a structured API error.

    Args:
        code: An ErrorCode enum value.
        message: Human-readable message for the client.
        status_code: HTTP status code (default 400).
        detail: Optional list of field-level details.
    """

    def __init__(
        self,
        code: ErrorCode,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: list[ErrorDetail] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.detail = detail


# ---------------------------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------------------------

def _get_request_id(request: Request) -> str | None:
    return request.headers.get("X-Request-ID") or request.state.__dict__.get("request_id")


def _make_error_response(
    code: str,
    message: str,
    status_code: int,
    request: Request,
    detail: list[ErrorDetail] | None = None,
) -> JSONResponse:
    envelope = ErrorResponse(
        error=ErrorEnvelope(
            code=code,
            message=message,
            detail=detail,
            request_id=_get_request_id(request),
        )
    )
    return JSONResponse(
        status_code=status_code,
        content=envelope.model_dump(exclude_none=True),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all structured exception handlers on the FastAPI app."""

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        logger.warning(
            "[v0] AppError code=%s message=%s request_id=%s",
            exc.code, exc.message, _get_request_id(request),
        )
        return _make_error_response(
            code=exc.code.value,
            message=exc.message,
            status_code=exc.status_code,
            request=request,
            detail=exc.detail,
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        code_map = {
            401: ErrorCode.UNAUTHORIZED,
            403: ErrorCode.FORBIDDEN,
            404: ErrorCode.NOT_FOUND,
            409: ErrorCode.CONFLICT,
            429: ErrorCode.RATE_LIMITED,
        }
        code = code_map.get(exc.status_code, ErrorCode.INTERNAL_ERROR)
        return _make_error_response(
            code=code.value,
            message=str(exc.detail),
            status_code=exc.status_code,
            request=request,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        detail = [
            ErrorDetail(
                field=" → ".join(str(loc) for loc in err.get("loc", [])),
                message=err.get("msg", "invalid"),
                value=err.get("input"),
            )
            for err in exc.errors()
        ]
        return _make_error_response(
            code=ErrorCode.VALIDATION_ERROR.value,
            message="Request validation failed",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            request=request,
            detail=detail,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        request_id = _get_request_id(request)
        logger.exception(
            "[v0] Unhandled exception request_id=%s path=%s",
            request_id, request.url.path,
        )
        return _make_error_response(
            code=ErrorCode.INTERNAL_ERROR.value,
            message="An unexpected error occurred. Please try again.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            request=request,
        )
