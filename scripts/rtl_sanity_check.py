#!/usr/bin/env python3
"""Lightweight RTL sanity checks for quick local validation."""

from __future__ import annotations

import argparse
import pathlib
import re

ASSIGN_RE = re.compile(r"\bassign\s+(\w+)\s*=")


def check_unconnected_prbs(file_contents: str, filename: str) -> list[str]:
    findings: list[str] = []
    if ".prbs_out()" in file_contents:
        findings.append(
            f"ERROR: {filename}: PRBS output left unconnected (.prbs_out())"
        )
    if ".trigger()" in file_contents:
        findings.append(
            f"ERROR: {filename}: PRBS trigger left unconnected (.trigger())"
        )
    return findings


def check_duplicate_assigns(
    file_contents: str,
    filename: str,
) -> list[str]:
    findings: list[str] = []
    targets: dict[str, int] = {}
    for match in ASSIGN_RE.finditer(file_contents):
        lhs = match.group(1)
        targets[lhs] = targets.get(lhs, 0) + 1
    duplicates = [name for name, count in targets.items() if count > 1]
    for lhs in sorted(duplicates):
        findings.append(f"ERROR: {filename}: duplicate continuous assign target: {lhs}")
    return findings


def check_missing_reset(file_contents: str, filename: str):
    if "always_ff" in file_contents and "rst_n" in file_contents:
        if "if (!rst_n)" not in file_contents:
            print(f"WARNING: {filename}: " "always_ff without explicit reset condition")


def check_implicit_width(file_contents: str, filename: str):
    pattern = re.compile(r"\bassign\s+\w+\s*=\s*\{\w+\}\s*;")
    for match in pattern.finditer(file_contents):
        print(
            f"NOTE: {filename}: implicit concatenation width may require "
            f"attention: {match.group(0)}"
        )


def check_generated_contamination(
    rtl_files: list[pathlib.Path],
) -> list[str]:
    findings: list[str] = []
    for path in rtl_files:
        if path.suffix == ".pyc":
            findings.append(f"ERROR: generated artifact in RTL tree: {path}")
        if "__pycache__" in path.parts:
            findings.append(f"ERROR: generated artifact in RTL tree: {path}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Run lightweight RTL checks.")
    parser.add_argument(
        "--rtl-dir",
        default="rtl",
        help="RTL directory to scan.",
    )
    args = parser.parse_args()

    rtl_dir = pathlib.Path(args.rtl_dir)
    if not rtl_dir.exists() or not rtl_dir.is_dir():
        print(f"ERROR: RTL directory not found: {rtl_dir}")
        return 1

    files = sorted(rtl_dir.glob("*.v"))
    if not files:
        print(f"ERROR: no RTL files found under {rtl_dir}")
        return 1

    errors: list[str] = []
    errors.extend(check_generated_contamination(files))

    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        check_missing_reset(text, path.name)
        check_implicit_width(text, path.name)
        errors.extend(check_duplicate_assigns(text, path.name))
        errors.extend(check_unconnected_prbs(text, path.name))

    for error in errors:
        print(error)

    if errors:
        print("Sanity check failed.")
        return 1

    print("Sanity check complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
