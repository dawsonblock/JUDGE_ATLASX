#!/usr/bin/env python3
"""CI script: check for prohibited direct outbound HTTP calls in source code.

Delegates to app.security.outbound_network_policy.check_source_violations.

Usage
-----
    python scripts/check_outbound_network_policy.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add backend to path so we can import the module
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.security.outbound_network_policy import check_source_violations


def main() -> int:
    repo_root = str(Path(__file__).parent.parent / "backend")
    violations = check_source_violations(repo_root=repo_root)

    if violations:
        print(f"[FAIL] {len(violations)} prohibited direct HTTP call(s) found:\n")
        for v in violations:
            print(f"  {v['file']}:{v['line']}")
            print(f"    Pattern: {v['pattern']}")
            print(f"    Code:    {v['snippet']}\n")
        print("Use app.security.safe_fetch instead of calling requests/httpx directly.")
        return 1

    print("[PASS] No prohibited direct HTTP calls found in source code.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
