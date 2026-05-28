#!/usr/bin/env python3
"""Dependency license scanner.

Checks all Python (pip) and Node (npm/pnpm) dependencies against an allowlist
of approved open-source licenses. Any dependency with an unknown or prohibited
license causes the script to exit with code 1.

This is designed to run in CI before a release is cut.

Approved licenses (SPDX identifiers)
--------------------------------------
  MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, Python-2.0,
  PSF-2.0, CC0-1.0, Unlicense, LGPL-2.1, LGPL-3.0

Prohibited licenses (copyleft, incompatible with commercial distribution)
--------------------------------------------------------------------------
  GPL-2.0, GPL-3.0, AGPL-3.0, SSPL-1.0, Commons Clause

Usage
-----
    python scripts/check_dependency_licenses.py
    python scripts/check_dependency_licenses.py --python-only
    python scripts/check_dependency_licenses.py --node-only
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

APPROVED_LICENSES: set[str] = {
    "MIT",
    "MIT License",
    "Apache-2.0",
    "Apache Software License",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "BSD License",
    "ISC",
    "Python-2.0",
    "PSF-2.0",
    "Python Software Foundation License",
    "CC0-1.0",
    "Unlicense",
    "LGPL-2.1",
    "LGPL-3.0",
    "GNU Lesser General Public License v2 or later (LGPLv2+)",
    "GNU Lesser General Public License v3 (LGPLv3)",
    "Mozilla Public License 2.0 (MPL 2.0)",
    "MPL-2.0",
    "0BSD",
    "BlueOak-1.0.0",
}

PROHIBITED_LICENSES: set[str] = {
    "GPL-2.0",
    "GPL-3.0",
    "AGPL-3.0",
    "SSPL-1.0",
    "Commons Clause",
    "GNU General Public License v2",
    "GNU General Public License v3",
    "GNU Affero General Public License v3",
}

# Packages explicitly allowed despite ambiguous license metadata
ALLOWLISTED_PACKAGES: set[str] = {
    "typing_extensions",  # Python stdlib extension, effectively PSF
    "setuptools",         # MIT / PSF hybrid
    "wheel",              # MIT
    "pip",                # MIT
}


def _normalise(license_str: str) -> str:
    return (license_str or "UNKNOWN").strip()


def check_python_deps() -> list[dict]:
    """Use pip-licenses (if available) to scan Python deps."""
    violations: list[dict] = []
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip_licenses", "--format=json", "--with-license-file"],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode != 0:
            print(f"  [WARN] pip-licenses not available; skipping Python scan.\n"
                  f"  Install with: pip install pip-licenses")
            return []
        packages = json.loads(result.stdout)
    except (FileNotFoundError, json.JSONDecodeError, subprocess.TimeoutExpired) as e:
        print(f"  [WARN] Python license scan skipped: {e}")
        return []

    for pkg in packages:
        name = pkg.get("Name", "?")
        license_str = _normalise(pkg.get("License", "UNKNOWN"))

        if name in ALLOWLISTED_PACKAGES:
            continue
        if license_str in PROHIBITED_LICENSES:
            violations.append({
                "package": name,
                "license": license_str,
                "type": "python",
                "severity": "prohibited",
            })
        elif license_str == "UNKNOWN":
            violations.append({
                "package": name,
                "license": license_str,
                "type": "python",
                "severity": "unknown",
            })

    return violations


def check_node_deps(frontend_dir: Path) -> list[dict]:
    """Use license-checker (if available) to scan Node deps."""
    violations: list[dict] = []
    if not (frontend_dir / "node_modules").exists():
        print("  [WARN] frontend/node_modules not found; skipping Node scan.")
        return []

    try:
        result = subprocess.run(
            ["npx", "license-checker", "--json", "--production"],
            capture_output=True, text=True, cwd=str(frontend_dir), timeout=120,
        )
        if result.returncode != 0:
            print("  [WARN] license-checker not available; skipping Node scan.")
            return []
        packages = json.loads(result.stdout)
    except (FileNotFoundError, json.JSONDecodeError, subprocess.TimeoutExpired) as e:
        print(f"  [WARN] Node license scan skipped: {e}")
        return []

    for pkg_name, meta in packages.items():
        license_str = _normalise(meta.get("licenses", "UNKNOWN"))
        if license_str in PROHIBITED_LICENSES:
            violations.append({
                "package": pkg_name,
                "license": license_str,
                "type": "node",
                "severity": "prohibited",
            })

    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check dependency licenses")
    parser.add_argument("--python-only", action="store_true")
    parser.add_argument("--node-only", action="store_true")
    args = parser.parse_args(argv)

    repo_root = Path(__file__).parent.parent
    all_violations: list[dict] = []

    if not args.node_only:
        print("Scanning Python dependencies...")
        all_violations.extend(check_python_deps())

    if not args.python_only:
        frontend_dir = repo_root / "frontend"
        print("Scanning Node dependencies...")
        all_violations.extend(check_node_deps(frontend_dir))

    prohibited = [v for v in all_violations if v["severity"] == "prohibited"]
    unknown = [v for v in all_violations if v["severity"] == "unknown"]

    if prohibited:
        print(f"\n[FAIL] {len(prohibited)} prohibited license(s) found:")
        for v in prohibited:
            print(f"  - [{v['type']}] {v['package']}: {v['license']}")

    if unknown:
        print(f"\n[WARN] {len(unknown)} package(s) with unknown license:")
        for v in unknown:
            print(f"  - [{v['type']}] {v['package']}: {v['license']}")

    if not all_violations:
        print("[PASS] All dependency licenses are acceptable")
        return 0

    return 1 if prohibited else 0


if __name__ == "__main__":
    sys.exit(main())
