#!/usr/bin/env python3
"""Fail-closed Node version gate for frontend proof.

Expected behavior:
- PASS when Node major matches required major
- If expected minor is provided, enforce exact major/minor match
- Emit clear mismatch message for proof logs
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys


def _parse_major_minor(node_version: str) -> tuple[int, int] | None:
    match = re.match(r"^v?(\d+)\.(\d+)", node_version.strip())
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Frontend Node version gate")
    parser.add_argument("--expected-major", type=int, default=20)
    parser.add_argument("--expected-minor", type=int)
    args = parser.parse_args()

    proc = subprocess.run(
        ["node", "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        print("Node executable not available")
        return 1

    version = proc.stdout.strip() or "unknown"
    parsed = _parse_major_minor(version)
    if parsed is None:
        print(f"Unable to parse Node version: {version}")
        return 1

    major, minor = parsed
    if major != args.expected_major:
        expected = f"{args.expected_major}.x"
        print(f"Frontend release gate requires Node {expected}. Current Node: {version}. Use nvm use {args.expected_major}.")
        return 1

    if args.expected_minor is not None and minor != args.expected_minor:
        expected = f"{args.expected_major}.{args.expected_minor}.x"
        print(f"Frontend release gate requires Node {expected}. Current Node: {version}. Use nvm use {args.expected_major}.{args.expected_minor}.")
        return 1

    print(f"Node gate PASS: {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
