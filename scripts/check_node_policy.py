#!/usr/bin/env python3
"""Validate the Node runtime against the declared frontend policy."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def _parse_version(version: str) -> tuple[int, int, int] | None:
    match = re.match(r"^v?(\d+)(?:\.(\d+))?(?:\.(\d+))?", version.strip())
    if not match:
        return None
    return (
        int(match.group(1)),
        int(match.group(2) or 0),
        int(match.group(3) or 0),
    )


def _compare_versions(left: tuple[int, int, int], right: tuple[int, int, int]) -> int:
    if left < right:
        return -1
    if left > right:
        return 1
    return 0


def _satisfies_range(version: str, spec: str) -> bool:
    parsed_version = _parse_version(version)
    if parsed_version is None:
        return False

    comparators = [token for token in spec.split() if token]
    for comparator in comparators:
        if comparator.startswith(">="):
            target = _parse_version(comparator[2:])
            if target is None or _compare_versions(parsed_version, target) < 0:
                return False
        elif comparator.startswith(">"):
            target = _parse_version(comparator[1:])
            if target is None or _compare_versions(parsed_version, target) <= 0:
                return False
        elif comparator.startswith("<="):
            target = _parse_version(comparator[2:])
            if target is None or _compare_versions(parsed_version, target) > 0:
                return False
        elif comparator.startswith("<"):
            target = _parse_version(comparator[1:])
            if target is None or _compare_versions(parsed_version, target) >= 0:
                return False
        else:
            target = _parse_version(comparator)
            if target is None or parsed_version != target:
                return False
    return True


def _run_version_command(command: list[str]) -> str:
    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or f"command failed: {' '.join(command)}")
    return proc.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(REPO_ROOT), help="Repository root")
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    root_nvmrc = repo_root / ".nvmrc"
    frontend_nvmrc = repo_root / "frontend" / ".nvmrc"
    package_json_path = repo_root / "frontend" / "package.json"

    root_major = _read_text(root_nvmrc)
    frontend_major = _read_text(frontend_nvmrc)
    package_json = json.loads(package_json_path.read_text(encoding="utf-8"))
    node_range = package_json.get("engines", {}).get("node")
    npm_range = package_json.get("engines", {}).get("npm")

    errors: list[str] = []
    if root_major != frontend_major:
        errors.append(f".nvmrc mismatch: root={root_major} frontend={frontend_major}")

    node_version = _run_version_command(["node", "--version"])
    npm_version = _run_version_command(["npm", "--version"])

    parsed_node = _parse_version(node_version)
    if parsed_node is None:
        errors.append(f"Unable to parse node version: {node_version}")
    else:
        if parsed_node[0] != int(root_major):
            errors.append(
                f"Node major mismatch: declared .nvmrc={root_major} but runtime is {node_version}"
            )
        if not isinstance(node_range, str) or not _satisfies_range(node_version, node_range):
            errors.append(
                f"Node runtime {node_version} does not satisfy frontend/package.json engines.node '{node_range}'"
            )

    if not isinstance(npm_range, str) or not _satisfies_range(npm_version, npm_range):
        errors.append(
            f"npm runtime {npm_version} does not satisfy frontend/package.json engines.npm '{npm_range}'"
        )

    print(f"NODE_VERSION: {node_version}")
    print(f"NPM_VERSION: {npm_version}")
    print(f"ROOT_NVMRC: {root_major}")
    print(f"FRONTEND_NVMRC: {frontend_major}")
    print(f"NODE_RANGE: {node_range}")
    print(f"NPM_RANGE: {npm_range}")

    if errors:
        print("NODE_POLICY: FAIL")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("NODE_POLICY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())