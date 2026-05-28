#!/usr/bin/env python3
"""Validate source/proof release archives for safety and required content."""

from __future__ import annotations

import argparse
from pathlib import PurePosixPath
from zipfile import ZipFile

REQUIRED_SOURCE = [
    "Makefile",
    "README.md",
    "rtl/axilite_regfile_full.v",
    "scripts/preboard_check.py",
    "tests/test_axilite_regfile_static.py",
]

FORBIDDEN_SOURCE_PREFIXES = [
    "__MACOSX/",
    "sim/build/",
]

FORBIDDEN_SOURCE_SUFFIXES = [
    ".pyc",
]

REQUIRED_PROOF = [
    "reports/preboard_local_summary.json",
    "reports/preboard_local_summary.md",
    "reports/implementation_gate_summary.json",
    "reports/implementation_gate_summary.md",
]


def unsafe_entry(name: str) -> bool:
    path = PurePosixPath(name)
    if path.is_absolute():
        return True
    return any(part == ".." for part in path.parts)


def single_root(entries: list[str]) -> tuple[bool, str]:
    roots = {
        PurePosixPath(entry).parts[0] for entry in entries if PurePosixPath(entry).parts
    }
    if len(roots) != 1:
        return False, ",".join(sorted(roots))
    return True, next(iter(roots))


def strip_root(entry: str) -> str:
    parts = PurePosixPath(entry).parts
    if len(parts) <= 1:
        return ""
    return PurePosixPath(*parts[1:]).as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate release archive.")
    parser.add_argument("archive", help="Path to .zip archive")
    parser.add_argument(
        "--mode",
        choices=["source", "proof"],
        required=True,
        help="Expected archive content mode.",
    )
    args = parser.parse_args()

    with ZipFile(args.archive, "r") as zf:
        names = [n for n in zf.namelist() if not n.endswith("/")]

    if not names:
        print("archive is empty")
        return 1

    for name in names:
        if unsafe_entry(name):
            print(f"unsafe zip entry: {name}")
            return 1

    ok_root, root_info = single_root(names)
    if not ok_root:
        print(f"archive has multiple roots: {root_info}")
        return 1

    rel_names = [strip_root(n) for n in names if strip_root(n)]
    rel_set = set(rel_names)

    if args.mode == "source":
        for req in REQUIRED_SOURCE:
            if req not in rel_set:
                print(f"missing required source entry: {req}")
                return 1

        for rel in rel_names:
            if any(rel.startswith(p) for p in FORBIDDEN_SOURCE_PREFIXES):
                print(f"forbidden source entry: {rel}")
                return 1
            if any(rel.endswith(s) for s in FORBIDDEN_SOURCE_SUFFIXES):
                print(f"forbidden source entry: {rel}")
                return 1

    else:
        for req in REQUIRED_PROOF:
            if req not in rel_set:
                print(f"missing required proof entry: {req}")
                return 1

    print(
        f"archive valid mode={args.mode} entries={len(rel_names)} " f"root={root_info}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
