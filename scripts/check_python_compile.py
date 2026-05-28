#!/usr/bin/env python3
"""Compile-check all Python files in the repository.

Discovers every .py file under the repo root (excluding virtual envs,
build artefacts, and generated directories) and runs py_compile on each.
Reports every file that fails, then exits non-zero if any failure occurred.

Usage:
    python scripts/check_python_compile.py [--root REPO_ROOT]

The compile check must cover:
    backend/app/**/*.py
    backend/scripts/**/*.py
    scripts/**/*.py
    backend/tests/**/*.py
    tests/**/*.py

Exit codes:
    0  all files compiled successfully
    1  one or more files have syntax errors
    2  bad arguments / root not found
"""

from __future__ import annotations

import argparse
import os
import py_compile
import sys
from pathlib import Path

# Directories to exclude entirely from discovery.
EXCLUDE_DIRS: frozenset[str] = frozenset(
    {
        ".venv",
        "venv",
        ".env",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "dist",
        "build",
        ".next",
        "coverage",
        ".git",
        "target",
    }
)


def _iter_python_files(root: Path):
    """Yield every .py file under root, skipping excluded directories."""
    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        # Prune excluded directories in-place so os.walk does not descend.
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for filename in filenames:
            if filename.endswith(".py"):
                yield Path(dirpath) / filename


def check(root: Path) -> int:
    """Compile every .py file under root.

    Returns the number of files that failed to compile.
    """
    failures: list[tuple[Path, str]] = []
    checked = 0

    for py_file in sorted(_iter_python_files(root)):
        checked += 1
        try:
            py_compile.compile(str(py_file), doraise=True)
        except py_compile.PyCompileError as exc:
            failures.append((py_file, str(exc)))

    if failures:
        print(f"FAIL: {len(failures)} file(s) failed to compile out of {checked}:")
        for path, msg in failures:
            rel = path.relative_to(root)
            print(f"  {rel}: {msg}")
        return len(failures)

    print(f"OK: all {checked} Python files compiled successfully under {root}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root to scan (default: current directory)",
    )
    args = parser.parse_args()
    root = Path(args.root).resolve()

    if not root.is_dir():
        print(f"ERROR: {root} is not a directory", file=sys.stderr)
        sys.exit(2)

    sys.exit(0 if check(root) == 0 else 1)


if __name__ == "__main__":
    main()
