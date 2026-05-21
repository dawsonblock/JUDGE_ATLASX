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


def _validate_stored_metadata(repo_root: Path, nvmrc_major: str) -> list[str]:
    """Check that stored proof metadata node version agrees with .nvmrc policy.

    Reads ``release_gate.json`` and ``proof_manifest.json`` in
    ``artifacts/proof/current/`` for a ``node_version`` field, then compares
    the major version against the declared ``.nvmrc`` major.  Also checks
    ``CURRENT_PROOF.md`` for a ``node_version:`` line.

    Args:
        repo_root: Repository root directory.
        nvmrc_major: Major version string declared in ``.nvmrc`` (e.g. ``"20"``).

    Returns:
        List of error strings.  Empty means all stored metadata agrees.
    """
    errors: list[str] = []

    proof_json_files = {
        "release_gate.json": repo_root / "artifacts" / "proof" / "current" / "release_gate.json",
        "proof_manifest.json": repo_root / "artifacts" / "proof" / "current" / "proof_manifest.json",
    }
    for label, path in proof_json_files.items():
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        stored_node = data.get("node_version") or data.get("gate_runner_node_version")
        if not stored_node or stored_node == "unknown":
            continue
        parsed_stored = _parse_version(stored_node)
        if parsed_stored is None:
            errors.append(
                f"{label}: unable to parse stored node_version '{stored_node}'"
            )
            continue
        try:
            declared_major = int(nvmrc_major)
        except ValueError:
            continue
        if parsed_stored[0] != declared_major:
            errors.append(
                f"{label}: stored node_version '{stored_node}' (major={parsed_stored[0]}) "
                f"disagrees with .nvmrc declared major={nvmrc_major}"
            )

    # Check doc files for node_version: lines
    doc_files = ["CURRENT_PROOF.md", "PROOF_STATUS.md", "STATUS.md"]
    for doc_name in doc_files:
        doc_path = repo_root / doc_name
        if not doc_path.exists():
            continue
        text = doc_path.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"-\s*node_version:\s*(v?\d+[\.\d]*)", text)
        if not match:
            continue
        doc_ver = match.group(1).strip()
        parsed_doc = _parse_version(doc_ver)
        if parsed_doc is None:
            continue
        try:
            declared_major = int(nvmrc_major)
        except ValueError:
            continue
        if parsed_doc[0] != declared_major:
            errors.append(
                f"{doc_name}: node_version '{doc_ver}' (major={parsed_doc[0]}) "
                f"disagrees with .nvmrc declared major={nvmrc_major}"
            )

    return errors


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

    # Validate stored proof metadata for node version drift
    metadata_errors = _validate_stored_metadata(repo_root, root_major)
    errors.extend(metadata_errors)

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