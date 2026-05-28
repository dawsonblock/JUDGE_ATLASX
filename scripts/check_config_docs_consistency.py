#!/usr/bin/env python3
"""Verify that documented env vars match real settings in code.

Fails if:
  1. A setting exists in code but is not documented in .env.example.
  2. A documented setting no longer exists in code.
  3. A production-dangerous default appears in production docs.
  4. An experimental feature is documented as safe without a WARNING.

Usage:
    python3 scripts/check_config_docs_consistency.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Settings fields that are intentionally undocumented (internal/computed)
SKIP_FIELDS = {
    "model_config",
    "app_name",
}

# Dangerous defaults — flag if present in production example without a SECURITY note
DANGEROUS_DEFAULTS = {
    "jwt_secret_key": "CHANGE-ME-BEFORE-PRODUCTION",
    "admin_token": None,
    "first_admin_secret": None,
}

# Experimental flags that must carry a WARNING if documented as safe
EXPERIMENTAL_FLAGS = {
    "enable_experimental_live_map",
    "enable_workflow_admin",
    "enable_public_platform",
    "enable_legacy_admin_token",
    "enable_legacy_us_ingest_routes",
}


def extract_config_fields(config_path: Path) -> set[str]:
    """Extract field names from pydantic Settings class."""
    fields: set[str] = set()
    in_class = False
    content = config_path.read_text()
    for line in content.splitlines():
        if "class Settings(" in line:
            in_class = True
            continue
        if in_class:
            # End of class
            if line.startswith("@") or (line.startswith("def ") and not line.startswith("    ")):
                break
            # Field declaration: "    field_name: type = ..."
            m = re.match(r"^\s{4}(\w+)\s*:", line)
            if m:
                name = m.group(1)
                if name not in SKIP_FIELDS and not name.startswith("_"):
                    fields.add(name)
    return fields


def extract_env_keys_from_example(path: Path, prefix: str = "JTA_") -> set[str]:
    """Extract env var keys from a .env.example file, strip prefix, lowercase."""
    keys: set[str] = set()
    if not path.exists():
        return keys
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key = line.split("=")[0].strip()
        if key.startswith(prefix):
            keys.add(key[len(prefix):].lower())
    return keys


def check_production_docs(prod_doc: Path) -> list[str]:
    """Check production docs for dangerous defaults without SECURITY notes."""
    issues: list[str] = []
    if not prod_doc.exists():
        return issues
    content = prod_doc.read_text()
    if "CHANGE-ME-BEFORE-PRODUCTION" in content:
        issues.append(
            f"{prod_doc}: Contains 'CHANGE-ME-BEFORE-PRODUCTION' — "
            "replace with a real secret or mark as required"
        )
    return issues


def check_experimental_docs(doc: Path) -> list[str]:
    """Check that experimental flags in docs have a WARNING."""
    issues: list[str] = []
    if not doc.exists():
        return issues
    content = doc.read_text()
    for flag in EXPERIMENTAL_FLAGS:
        env_name = f"JTA_{flag.upper()}"
        if env_name in content:
            # The flag is mentioned — check for a warning nearby
            idx = content.find(env_name)
            surrounding = content[max(0, idx - 200): idx + 200].lower()
            if "warn" not in surrounding and "experimental" not in surrounding and "alpha" not in surrounding:
                issues.append(
                    f"{doc}: {env_name} mentioned without WARN/experimental/alpha context"
                )
    return issues


def main() -> int:
    config_path = REPO_ROOT / "backend" / "app" / "core" / "config.py"
    env_example = REPO_ROOT / ".env.example"
    backend_env_example = REPO_ROOT / "backend" / ".env.example"
    prod_doc = REPO_ROOT / ".env.example.production"
    setup_doc = REPO_ROOT / "docs" / "setup" / "MACOS_VSCODE_ALPHA_SETUP.md"

    issues: list[str] = []

    if not config_path.exists():
        print(f"FAIL: Config file not found: {config_path}")
        return 1

    code_fields = extract_config_fields(config_path)
    root_keys = extract_env_keys_from_example(env_example)
    backend_keys = extract_env_keys_from_example(backend_env_example)
    documented_keys = root_keys | backend_keys

    # 1. Fields in code but not documented
    undocumented = code_fields - documented_keys
    for field in sorted(undocumented):
        issues.append(f"UNDOCUMENTED: JTA_{field.upper()} exists in config but not in .env.example")

    # 2. Keys in .env.example that don't match any config field
    stale = documented_keys - code_fields
    for key in sorted(stale):
        issues.append(f"STALE: JTA_{key.upper()} in .env.example but not in Settings")

    # 3. Production-dangerous defaults in prod docs
    issues.extend(check_production_docs(prod_doc))

    # 4. Experimental flags without warnings in setup docs
    issues.extend(check_experimental_docs(setup_doc))

    print("\nConfig/Docs Consistency Check")
    print("=" * 50)
    print(f"Config fields:   {len(code_fields)}")
    print(f"Documented keys: {len(documented_keys)}")

    if issues:
        print(f"\n{len(issues)} issue(s) found:\n")
        for issue in issues:
            print(f"  {issue}")
        return 1

    print("\nPASS: Config and docs are consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
