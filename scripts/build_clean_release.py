#!/usr/bin/env python3
"""Build clean alpha runtime release archive.

Produces:
- JUDGE_ATLASX-alpha-clean.zip
- artifacts/proof/current/RELEASE_MANIFEST.json
- Optional JUDGE_ATLASX-reference-bundle.zip (external references only)
"""

from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_ZIP = REPO_ROOT / "JUDGE_ATLASX-alpha-clean.zip"
REF_ZIP = REPO_ROOT / "JUDGE_ATLASX-reference-bundle.zip"
MANIFEST_PATH = REPO_ROOT / "artifacts" / "proof" / "current" / "RELEASE_MANIFEST.json"

INCLUDED_DIRS = [
    "backend",
    "frontend",
    "docs",
    "deploy",
    "scripts",
    "tests",
    "tools",
    "artifacts/proof/current",
]

EXCLUDED_DIR_MARKERS = {
    "external_reference",
    "artifacts/old",
    "artifacts/archive",
    "artifacts/history",
    "generated_logs",
    "tmp",
    "cache",
    "old_phase_reports",
    "duplicate_status_docs",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".next",
    "dist",
    "coverage",
    ".git",
    ".venv",
    "venv",
    "docs/archive",
    "legacy_disabled",
    "reference_only",
    "reports",
    "research",
    "skills",
}

EXCLUDED_FILE_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".log",
    ".tsbuildinfo",
}


def _git_commit() -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT)
        return out.decode("utf-8").strip()
    except Exception:
        return "unknown"


def _is_excluded(path: Path) -> bool:
    rel = path.relative_to(REPO_ROOT)
    rel_text = rel.as_posix()

    for marker in EXCLUDED_DIR_MARKERS:
        if rel_text == marker or rel_text.startswith(marker + "/"):
            return True

    if any(part in EXCLUDED_DIR_MARKERS for part in rel.parts):
        return True

    if path.suffix.lower() in EXCLUDED_FILE_SUFFIXES:
        return True

    return False


def _build_reference_bundle() -> str | None:
    ref_dir = REPO_ROOT / "external_reference"
    if not ref_dir.exists():
        return None

    if REF_ZIP.exists():
        REF_ZIP.unlink()

    with ZipFile(REF_ZIP, "w", compression=ZIP_DEFLATED) as zf:
        for path in ref_dir.rglob("*"):
            if path.is_dir():
                continue
            arcname = path.relative_to(REPO_ROOT).as_posix()
            zf.write(path, arcname)

    return REF_ZIP.name


def _write_release_manifest(file_count: int, reference_bundle: str | None) -> dict:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "release_mode": "alpha",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": _git_commit(),
        "included_directories": INCLUDED_DIRS,
        "excluded_directories": sorted(EXCLUDED_DIR_MARKERS),
        "file_count": file_count,
        "proof_scope": [
            "backend tests",
            "frontend contract tests",
            "runtime boundary validation",
            "source registry validation",
            "evidence store validation",
            "ingestion replay tests",
            "security startup blocker tests",
            "publication gate tests",
        ],
        "optional_reference_bundle": reference_bundle,
    }
    MANIFEST_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    if OUT_ZIP.exists():
        OUT_ZIP.unlink()

    reference_bundle = _build_reference_bundle()

    file_count = 0

    # Write manifest first so it gets included in archive.
    _write_release_manifest(file_count=0, reference_bundle=reference_bundle)

    with ZipFile(OUT_ZIP, "w", compression=ZIP_DEFLATED) as zf:
        for rel_dir in INCLUDED_DIRS:
            root = REPO_ROOT / rel_dir
            if not root.exists():
                continue
            for path in root.rglob("*"):
                if path.is_dir() or _is_excluded(path):
                    continue
                if path.resolve() == MANIFEST_PATH.resolve():
                    continue
                arcname = path.relative_to(REPO_ROOT).as_posix()
                zf.write(path, arcname)
                file_count += 1

    payload = _write_release_manifest(file_count=file_count, reference_bundle=reference_bundle)

    # Ensure updated manifest file count is in the zip.
    with ZipFile(OUT_ZIP, "a", compression=ZIP_DEFLATED) as zf:
        zf.write(MANIFEST_PATH, MANIFEST_PATH.relative_to(REPO_ROOT).as_posix())

    print(f"release archive: {OUT_ZIP}")
    print(f"release manifest: {MANIFEST_PATH}")
    if reference_bundle:
        print(f"reference bundle: {REF_ZIP}")
    print(f"files included: {payload['file_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
