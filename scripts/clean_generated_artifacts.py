#!/usr/bin/env python3
"""Remove generated artifacts used by local validation flows."""

from __future__ import annotations

import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

GENERATED_ARTIFACTS = [
    "rtl/reciprocal_lut_w16_q24w25.mem",
    "reciprocal_lut_w16_q24w25.mem",
    "sim/gkp_cosim_vectors.hex",
    "register_map.json",
    "register_map.md",
    "register_map_issues.log",
    "cdc_crossing_suggestions.json",
    "cdc_crossing_suggestions.md",
]


def clean_generated_artifacts(*, verbose: bool = False) -> list[Path]:
    removed: list[Path] = []
    for rel in GENERATED_ARTIFACTS:
        path = PROJECT_ROOT / rel
        if path.exists():
            path.unlink()
            removed.append(path)
            if verbose:
                print(f"removed {path.relative_to(PROJECT_ROOT)}")
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove generated local-validation artifacts."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print each removed file.",
    )
    args = parser.parse_args()

    removed = clean_generated_artifacts(verbose=args.verbose)
    print(f"removed_count={len(removed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
