#!/usr/bin/env python3
"""Run board smoke checks and emit summary reports."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from checks import (
    axi_lite_smoke,
    axis_capture_smoke,
    config_apply_smoke,
    ensure_capture_placeholders,
    prbs_capture_smoke,
    read_build_id,
    safety_trip_smoke,
    telemetry_window_smoke,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def markdown_summary(results: list[dict[str, object]], passed: bool) -> str:
    lines = [
        "# Board Smoke Summary",
        "",
        f"Timestamp UTC: `{utc_now()}`",
        f"Overall pass: **{passed}**",
        "",
        "| Check | Status | Pass | Reason |",
        "|---|---|---:|---|",
    ]
    for item in results:
        lines.append(
            f"| {item['name']} | {item['status']} | {item['pass']} | {item.get('reason', '')} |"
        )
    lines.append("")
    lines.append(
        "This scaffold is fail-closed until a real board adapter is wired."
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run board smoke scaffold checks.")
    parser.add_argument(
        "--device",
        default="",
        help="Board device identifier used by transport adapter (future).",
    )
    parser.add_argument(
        "--reports-dir",
        default="reports",
        help="Directory to write board smoke outputs.",
    )
    args = parser.parse_args()

    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    checks = [
        read_build_id,
        axi_lite_smoke,
        config_apply_smoke,
        safety_trip_smoke,
        prbs_capture_smoke,
        axis_capture_smoke,
        telemetry_window_smoke,
    ]
    results = [check(args.device or None) for check in checks]

    overall_pass = all(bool(item.get("pass", False)) for item in results)

    ensure_capture_placeholders(reports_dir)

    summary = {
        "timestamp_utc": utc_now(),
        "device": args.device,
        "pass": overall_pass,
        "checks": results,
        "capture_artifacts": {
            "prbs_hex": str((reports_dir / "board_capture_prbs.hex").as_posix()),
            "packets_jsonl": str((reports_dir / "board_capture_packets.jsonl").as_posix()),
        },
    }

    json_path = reports_dir / "board_smoke_summary.json"
    md_path = reports_dir / "board_smoke_summary.md"
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    md_path.write_text(markdown_summary(results, overall_pass), encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print("board-smoke-pass" if overall_pass else "board-smoke-fail")
    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
