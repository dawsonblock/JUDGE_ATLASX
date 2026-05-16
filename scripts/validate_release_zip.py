#!/usr/bin/env python3
"""Validate clean alpha release zip contents."""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZipFile

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ZIP = REPO_ROOT / "JUDGE_ATLASX-alpha-clean.zip"

REQUIRED_PREFIXES = [
    "backend/",
    "frontend/",
    "docs/",
    "deploy/",
    "scripts/",
    "artifacts/current/",
]

FORBIDDEN_MARKERS = [
    "external_reference/",
    "artifacts/old/",
    "artifacts/archive/",
    "artifacts/history/",
    "generated_logs/",
    "tmp/",
    "cache/",
    "node_modules/",
    "__pycache__/",
    ".pytest_cache/",
    ".next/",
    "dist/",
    "coverage/",
    ".git/",
    ".venv/",
    "venv/",
    "docs/archive/",
    "legacy_disabled/",
    "reference_only/",
]


def _path_has_marker(path: str, marker: str) -> bool:
    path_parts = [p for p in path.strip("/").split("/") if p]
    marker_parts = [p for p in marker.strip("/").split("/") if p]
    if not marker_parts:
        return False
    if len(marker_parts) == 1:
        return marker_parts[0] in path_parts
    for i in range(0, len(path_parts) - len(marker_parts) + 1):
        if path_parts[i : i + len(marker_parts)] == marker_parts:
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", dest="zip_path", default=str(DEFAULT_ZIP))
    args = parser.parse_args()

    zip_path = Path(args.zip_path)
    if not zip_path.exists():
        print(f"FAIL: zip not found: {zip_path}")
        return 1

    with ZipFile(zip_path, "r") as zf:
        names = zf.namelist()

    missing = [p for p in REQUIRED_PREFIXES if not any(n.startswith(p) for n in names)]
    forbidden = []
    for n in names:
        for marker in FORBIDDEN_MARKERS:
            if _path_has_marker(n, marker):
                forbidden.append(n)
                break

    if missing or forbidden:
        print("release zip validation: FAIL")
        for req in missing:
            print(f" - missing required path prefix: {req}")
        for bad in forbidden[:200]:
            print(f" - forbidden path in zip: {bad}")
        if len(forbidden) > 200:
            print(f" - ... and {len(forbidden) - 200} more forbidden entries")
        return 1

    print("release zip validation: PASS")
    print(f"validated zip: {zip_path}")
    print(f"entries: {len(names)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
