"""Outbound network access policy enforcement.

All outbound HTTP calls from the backend MUST go through ``safe_fetch`` (which
calls this module) or through the ``AllowedHostFetcher`` wrapper. Direct use
of ``requests``, ``httpx``, or ``aiohttp`` in application code is prohibited.

This module defines:
  - The allowlist of permitted outbound hostnames
  - Runtime enforcement that raises ``NetworkPolicyViolation`` on violations
  - A CI/lint-time checker (``check_violations``) that scans source files
    for prohibited direct HTTP calls

Allowlisted hosts (environment-specific overrides possible via env var
``JTA_ALLOWED_FETCH_HOSTS``)
----------------------------------------------------------------------
  laws-lois.justice.gc.ca        – Justice Canada XML/HTML feeds
  open.canada.ca                 – Federal open data portal
  canlii.org                     – CanLII API
  data.saskatoon.ca              – Saskatoon Open Data
  data.winnipeg.ca               – Winnipeg Open Data
  openregina.ca                  – Regina Open Data
  data.princealbertpolice.ca     – Prince Albert Police
  data.rcmp-grc.gc.ca            – RCMP open data
  newsapi.org                    – NewsAPI (when NEWSAPI_KEY is set)

Usage
-----
    from app.security.outbound_network_policy import enforce_host

    enforce_host("laws-lois.justice.gc.ca")   # OK
    enforce_host("evil.example.com")           # raises NetworkPolicyViolation
"""

from __future__ import annotations

import logging
import os
import re
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

# Default allowlist — can be extended via env var (comma-separated)
_DEFAULT_ALLOWED_HOSTS: frozenset[str] = frozenset(
    {
        "laws-lois.justice.gc.ca",
        "open.canada.ca",
        "canlii.org",
        "api.canlii.org",
        "data.saskatoon.ca",
        "data.winnipeg.ca",
        "openregina.ca",
        "data.rcmp-grc.gc.ca",
        "newsapi.org",
        # Internal: allow localhost in dev/test
        "localhost",
        "127.0.0.1",
    }
)

# Prohibited patterns in source code (for CI scanner)
_PROHIBITED_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("requests.get", re.compile(r"\brequests\.(get|post|put|patch|delete|head)\s*\(")),
    ("requests.Session", re.compile(r"\brequests\.Session\(\)")),
    ("httpx.get", re.compile(r"\bhttpx\.(get|post|put|patch|delete|head)\s*\(")),
    ("httpx.AsyncClient direct", re.compile(r"\bhttpx\.AsyncClient\(\)")),
    ("aiohttp.ClientSession direct", re.compile(r"\baiohttp\.ClientSession\(\)")),
    ("urllib.request.urlopen", re.compile(r"\burllib\.request\.urlopen\s*\(")),
]

# Files that are explicitly allowed to use httpx directly
_FETCH_ALLOWLIST_MODULES = frozenset(
    {
        "app/security/safe_fetch.py",
        "app/ingestion/base_adapter.py",
        "tests/",
    }
)


class NetworkPolicyViolation(Exception):
    """Raised when an outbound request targets a non-allowlisted host."""


def _get_allowed_hosts() -> frozenset[str]:
    """Read allowed hosts from env override or use defaults."""
    extra = os.getenv("JTA_ALLOWED_FETCH_HOSTS", "")
    if extra:
        extra_hosts = frozenset(h.strip() for h in extra.split(",") if h.strip())
        return _DEFAULT_ALLOWED_HOSTS | extra_hosts
    return _DEFAULT_ALLOWED_HOSTS


def enforce_host(host_or_url: str) -> None:
    """Raise NetworkPolicyViolation if the host is not on the allowlist.

    Args:
        host_or_url: Either a bare hostname (e.g. "laws-lois.justice.gc.ca")
                     or a full URL (e.g. "https://laws-lois.justice.gc.ca/...").
    """
    if "://" in host_or_url:
        parsed = urlparse(host_or_url)
        host = parsed.hostname or ""
    else:
        host = host_or_url.lower().split(":")[0]

    allowed = _get_allowed_hosts()
    if host not in allowed:
        logger.error("[v0] NetworkPolicyViolation: blocked outbound request to %s", host)
        raise NetworkPolicyViolation(
            f"Outbound request to '{host}' is not on the allowlist. "
            "Add it to JTA_ALLOWED_FETCH_HOSTS or the default allowlist in "
            "app/security/outbound_network_policy.py after security review."
        )


def check_source_violations(repo_root: str = ".") -> list[dict]:
    """Scan Python source files for prohibited direct HTTP calls.

    Returns a list of violation dicts with keys: file, line, pattern, snippet.
    This is intended to be called from CI or a pre-commit hook.
    """
    import pathlib

    violations: list[dict] = []
    root = pathlib.Path(repo_root)

    for py_file in root.rglob("*.py"):
        rel = str(py_file.relative_to(root))

        # Skip explicitly allowed modules
        if any(rel.startswith(allowed) for allowed in _FETCH_ALLOWLIST_MODULES):
            continue

        try:
            lines = py_file.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue

        for lineno, line in enumerate(lines, start=1):
            for pattern_name, pattern in _PROHIBITED_PATTERNS:
                if pattern.search(line):
                    violations.append(
                        {
                            "file": rel,
                            "line": lineno,
                            "pattern": pattern_name,
                            "snippet": line.strip(),
                        }
                    )

    return violations
