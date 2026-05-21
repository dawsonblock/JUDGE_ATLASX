#!/usr/bin/env python3
"""Staging proof for Saskatchewan CanLII machine-ingest sources.

This script validates a small fetch path for:
- sk_courts_qb_decisions (skkb)
- sk_courts_ca_decisions (skca)

Behavior:
- If CANLII_API_KEY is absent, exits 0 with explicit SKIPPED status.
- If CANLII_API_KEY is present, runs bounded sample fetches and verifies
  machine-ingest contract signals (raw snapshot, parser version, review-only).
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(REPO_ROOT, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.ingestion.source_adapters.canlii_api import CanLIIApiAdapter  # noqa: E402


@dataclass
class StagingCheck:
    source_key: str
    database: str


def _validate_result(source_key: str, result) -> list[str]:
    errors: list[str] = []
    if result.created_records:
        errors.append("created_records_must_be_empty")
    if result.parser_version is None:
        errors.append("missing_parser_version")
    if not result.fetch_url:
        errors.append("missing_fetch_url")
    if not result.raw_snapshot_bytes:
        errors.append("missing_raw_snapshot_bytes")
    if result.errors:
        errors.extend(f"adapter_error:{err}" for err in result.errors)
    if any(item.payload.get("public_visibility") == "public" for item in result.review_items):
        errors.append("review_item_attempted_public_visibility")

    if errors:
        print(f"CANLII_STAGING_{source_key.upper()}=FAIL:{'|'.join(errors)}")
    else:
        print(
            f"CANLII_STAGING_{source_key.upper()}=PASS:"
            f"review_items={len(result.review_items)}"
        )
    return errors


def main() -> int:
    api_key = os.getenv("CANLII_API_KEY", "").strip()
    if not api_key:
        print("CANLII_STAGING_STATUS=SKIPPED_NO_API_KEY")
        print(
            "CANLII_STAGING_NOTE="
            "CANLII_API_KEY is not configured; staging proof intentionally skipped"
        )
        return 0

    checks = [
        StagingCheck("sk_courts_qb_decisions", "skkb"),
        StagingCheck("sk_courts_ca_decisions", "skca"),
    ]

    failures: list[str] = []
    for check in checks:
        adapter = CanLIIApiAdapter(
            source_key=check.source_key,
            base_url="https://api.canlii.org/v1",
            api_key=api_key,
            allowed_domains_json='["api.canlii.org", "canlii.org", "www.canlii.org"]',
            public_record_authority="official_court_record",
            databases=[check.database],
            result_count=1,
            offset=0,
        )
        result = adapter.run()
        failures.extend(f"{check.source_key}:{reason}" for reason in _validate_result(check.source_key, result))

    if failures:
        print("CANLII_STAGING_STATUS=FAIL")
        for failure in failures:
            print(f"CANLII_STAGING_FAILURE={failure}")
        return 1

    print("CANLII_STAGING_STATUS=PASS")
    print("CANLII_STAGING_NO_AUTO_PUBLICATION=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
