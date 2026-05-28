"""Structured logging configuration for JUDGE_ATLASX.

Configures Python logging to emit JSON-structured lines in production and
human-readable coloured output in development. The format includes:

  - timestamp (ISO 8601)
  - level
  - logger name
  - message
  - request_id (when RequestIDMiddleware is active)
  - exc_info (when an exception is attached)

Usage in main.py:
    from app.core.logging_config import configure_logging
    configure_logging()
"""

from __future__ import annotations

import json
import logging
import sys
import traceback
from datetime import datetime, timezone


class _JSONFormatter(logging.Formatter):
    """Emit one JSON object per log record."""

    def format(self, record: logging.LogRecord) -> str:
        log_obj: dict = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Inject request_id if RequestIDMiddleware set it
        request_id = getattr(record, "request_id", None)
        if request_id:
            log_obj["request_id"] = request_id

        # Include exception info when present
        if record.exc_info:
            log_obj["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(log_obj, ensure_ascii=False)


class _DevFormatter(logging.Formatter):
    """Colourised, human-readable format for local development."""

    LEVEL_COLOURS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        colour = self.LEVEL_COLOURS.get(record.levelname, "")
        request_id = getattr(record, "request_id", None)
        rid_suffix = f" [{request_id}]" if request_id else ""
        msg = f"{colour}{record.levelname:8s}{self.RESET} {record.name}{rid_suffix}: {record.getMessage()}"
        if record.exc_info:
            msg += "\n" + self.formatException(record.exc_info)
        return msg


def configure_logging(
    level: str = "INFO",
    json_logs: bool | None = None,
) -> None:
    """Configure the root logger.

    Args:
        level: Log level name (e.g. "INFO", "DEBUG").
        json_logs: If True, emit JSON. If None, auto-detect from APP_ENV.
    """
    import os

    if json_logs is None:
        app_env = os.getenv("APP_ENV", "development")
        json_logs = app_env in ("production", "staging")

    formatter = _JSONFormatter() if json_logs else _DevFormatter()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Remove existing handlers to avoid duplicates on hot-reload
    root.handlers.clear()
    root.addHandler(handler)

    # Silence overly verbose third-party loggers
    for noisy_logger in ("sqlalchemy.engine", "uvicorn.access", "httpx"):
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)
