#!/usr/bin/env python3
"""Validate FINAL_RELEASE_HANDOFF claims against the actual release archive."""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import re

PATH_PATTERN = re.compile(r"^\s*-\s*Path:\s*(.+?)\s*$", re.IGNORECASE)
SHA_PATTERN = re.compile(
    r"^\s*-\s*SHA-256:\s*([0-9a-fA-F]{64})\s*$",
    re.IGNORECASE,
)


def _compute_sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _extract_claims(
    handoff_path: pathlib.Path,
) -> tuple[str | None, str | None]:
    claimed_path: str | None = None
    claimed_sha: str | None = None
    content = handoff_path.read_text(encoding="utf-8", errors="ignore")
    for line in content.splitlines():
        if claimed_path is None:
            match = PATH_PATTERN.match(line)
            if match:
                claimed_path = match.group(1).strip()
        if claimed_sha is None:
            match = SHA_PATTERN.match(line)
            if match:
                claimed_sha = match.group(1).lower()
        if claimed_path and claimed_sha:
            break
    return claimed_path, claimed_sha


def validate_handoff(
    repo_root: pathlib.Path,
    archive_path: pathlib.Path,
    handoff_path: pathlib.Path,
) -> tuple[bool, list[str]]:
    errors: list[str] = []

    if not handoff_path.exists() or not handoff_path.is_file():
        errors.append(f"handoff_not_found:{handoff_path}")
        return False, errors

    if not archive_path.exists() or not archive_path.is_file():
        errors.append(f"archive_not_found:{archive_path}")
        return False, errors

    claimed_path, claimed_sha = _extract_claims(handoff_path)
    if not claimed_path:
        errors.append("missing_claimed_path")
    if not claimed_sha:
        errors.append("missing_claimed_sha256")

    actual_sha = _compute_sha256(archive_path)

    if claimed_sha and claimed_sha != actual_sha:
        errors.append(
            f"sha256_mismatch:claimed={claimed_sha}:actual={actual_sha}"
        )

    if claimed_path:
        claimed_archive = pathlib.Path(claimed_path)
        if not claimed_archive.is_absolute():
            claimed_archive = (repo_root / claimed_archive).resolve()
        else:
            claimed_archive = claimed_archive.resolve()

        if claimed_archive != archive_path.resolve():
            errors.append(
                "archive_path_mismatch:"
                f"claimed={claimed_archive}:actual={archive_path.resolve()}"
            )

        if not claimed_archive.exists() or not claimed_archive.is_file():
            errors.append(f"claimed_archive_missing:{claimed_archive}")

    return len(errors) == 0, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument(
        "--archive",
        required=True,
        help="Archive path to verify",
    )
    parser.add_argument(
        "--handoff",
        default="FINAL_RELEASE_HANDOFF.md",
        help="Path to release handoff markdown",
    )
    args = parser.parse_args()

    repo_root = pathlib.Path(args.root).resolve()
    archive_path = pathlib.Path(args.archive)
    if not archive_path.is_absolute():
        archive_path = (repo_root / archive_path).resolve()
    handoff_path = pathlib.Path(args.handoff)
    if not handoff_path.is_absolute():
        handoff_path = (repo_root / handoff_path).resolve()

    ok, errors = validate_handoff(repo_root, archive_path, handoff_path)
    if ok:
        print("HANDOFF_CONSISTENCY: PASS")
        print(f"handoff={handoff_path.relative_to(repo_root)}")
        print(f"archive={archive_path.relative_to(repo_root)}")
        print(f"sha256={_compute_sha256(archive_path)}")
        return 0

    print("HANDOFF_CONSISTENCY: FAIL")
    print(f"handoff={handoff_path}")
    print(f"archive={archive_path}")
    for err in errors:
        print(f"ERROR: {err}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
