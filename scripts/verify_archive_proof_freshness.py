#!/usr/bin/env python3
"""Verify that a release archive is self-consistent and proof-complete.

Given a distributable ZIP produced by ``scripts/build_release_archive.py``,
this script checks:

1. The archive is parseable and contains an embedded ``release_gate.json``.
2. ``alpha_gate_passed`` is ``true`` in that JSON.
3. Every log_path referenced in ``proof_commands[*].log_path`` is present
   inside the ZIP.
4. No forbidden working-tree paths are present in the archive.

Exit codes:
  0 — all checks pass
  1 — one or more checks failed (details printed to stdout)

Usage::

    python3 scripts/verify_archive_proof_freshness.py --archive dist/JUDGE_ATLASX-main.clean.zip
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path


FORBIDDEN_PREFIXES = (
    "external_reference/",
    "artifacts/history/",
    ".trunk/",
)
FORBIDDEN_FILE_NAMES = {
    ".coverage",
}
# Forbidden path prefix variants under any root dir (e.g. JUDGE-main/external_reference/)
FORBIDDEN_INNER_SEGMENTS = (
    "/external_reference/",
    "/artifacts/history/",
    "/.trunk/",
)


def _find_gate_json(zf: zipfile.ZipFile) -> dict | None:
    """Locate release_gate.json inside the ZIP, under any top-level directory."""
    candidates = [
        name for name in zf.namelist()
        if name.endswith("artifacts/proof/current/release_gate.json")
    ]
    if not candidates:
        return None
    with zf.open(candidates[0]) as fh:
        try:
            return json.loads(fh.read().decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None


def verify_archive(archive_path: Path) -> list[str]:
    """Run all checks against a release archive ZIP.

    Returns:
        List of human-readable failure strings.  Empty list means all PASS.
    """
    failures: list[str] = []

    if not archive_path.exists():
        return [f"archive not found: {archive_path}"]

    try:
        zf = zipfile.ZipFile(archive_path, "r")
    except zipfile.BadZipFile as exc:
        return [f"archive is not a valid ZIP: {exc}"]

    with zf:
        names = zf.namelist()
        names_set = set(names)

        # 1. Locate and parse embedded release_gate.json
        payload = _find_gate_json(zf)
        if payload is None:
            failures.append(
                "release_gate.json not found in archive (expected at "
                "<root>/artifacts/proof/current/release_gate.json)"
            )
        else:
            # 2. alpha_gate_passed must be true
            if not payload.get("alpha_gate_passed"):
                failures.append(
                    f"alpha_gate_passed is not true in release_gate.json "
                    f"(got: {payload.get('alpha_gate_passed')!r})"
                )

            # 3. Every referenced log_path must exist in the archive
            missing_logs: list[str] = []
            for entry in payload.get("checks", []):
                log_path = entry.get("log_path")
                if not log_path or not isinstance(log_path, str):
                    continue
                # The archive nests under a root dir name, so look for any
                # name that ends with the expected relative path.
                found = any(
                    n.endswith("/" + log_path) or n == log_path
                    for n in names_set
                )
                if not found:
                    missing_logs.append(log_path)
            if missing_logs:
                failures.append(
                    f"{len(missing_logs)} proof log(s) referenced in "
                    f"release_gate.json checks are absent from the archive:"
                )
                for p in sorted(missing_logs):
                    failures.append(f"  missing: {p}")

        # 4. Forbidden working-tree paths must be absent
        for name in names:
            # Strip the root dir prefix (first segment) for prefix matching
            parts = name.split("/", 1)
            inner = parts[1] if len(parts) > 1 else name

            if any(inner.startswith(fp) for fp in FORBIDDEN_PREFIXES):
                failures.append(f"forbidden path in archive: {name}")
                continue

            file_name = Path(name).name
            if file_name in FORBIDDEN_FILE_NAMES:
                failures.append(f"forbidden file in archive: {name}")
                continue

            for seg in FORBIDDEN_INNER_SEGMENTS:
                if seg in ("/" + name + "/") or ("/" + inner).startswith(seg):
                    failures.append(f"forbidden segment in archive: {name}")
                    break

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--archive",
        required=True,
        help="Path to the release ZIP archive to verify",
    )
    args = parser.parse_args()

    archive_path = Path(args.archive).resolve()
    print(f"Verifying archive: {archive_path}")

    failures = verify_archive(archive_path)

    if failures:
        print(f"ARCHIVE_PROOF_FRESHNESS: FAIL ({len(failures)} issue(s))")
        for failure in failures:
            print(f"  {failure}")
        return 1

    print("ARCHIVE_PROOF_FRESHNESS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
