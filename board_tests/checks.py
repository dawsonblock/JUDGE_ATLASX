#!/usr/bin/env python3
"""Transport-agnostic board smoke checks scaffold.

These checks intentionally fail-closed until hardware adapter integration is
implemented. They still emit structured evidence so the flow is auditable.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def blocked_result(name: str, reason: str) -> dict[str, object]:
    return {
        "name": name,
        "pass": False,
        "status": "blocked",
        "timestamp_utc": utc_now(),
        "reason": reason,
    }


def read_build_id(device: str | None) -> dict[str, object]:
    return blocked_result(
        "read_build_id",
        f"device={device or 'unset'}: hardware adapter not implemented",
    )


def axi_lite_smoke(device: str | None) -> dict[str, object]:
    return blocked_result(
        "axi_lite_smoke",
        f"device={device or 'unset'}: AXI-Lite adapter not implemented",
    )


def config_apply_smoke(device: str | None) -> dict[str, object]:
    return blocked_result(
        "config_apply_smoke",
        f"device={device or 'unset'}: config apply adapter not implemented",
    )


def safety_trip_smoke(device: str | None) -> dict[str, object]:
    return blocked_result(
        "safety_trip_smoke",
        f"device={device or 'unset'}: safety stimulus adapter not implemented",
    )


def prbs_capture_smoke(device: str | None) -> dict[str, object]:
    return blocked_result(
        "prbs_capture_smoke",
        f"device={device or 'unset'}: PRBS capture adapter not implemented",
    )


def axis_capture_smoke(device: str | None) -> dict[str, object]:
    return blocked_result(
        "axis_capture_smoke",
        f"device={device or 'unset'}: AXIS capture adapter not implemented",
    )


def telemetry_window_smoke(device: str | None) -> dict[str, object]:
    return blocked_result(
        "telemetry_window_smoke",
        f"device={device or 'unset'}: telemetry adapter not implemented",
    )


def ensure_capture_placeholders(reports_dir: Path) -> None:
    reports_dir.mkdir(parents=True, exist_ok=True)

    prbs_path = reports_dir / "board_capture_prbs.hex"
    if not prbs_path.exists():
        prbs_path.write_text(
            "# Placeholder until board capture adapter is integrated\n",
            encoding="utf-8",
        )

    axis_path = reports_dir / "board_capture_packets.jsonl"
    if not axis_path.exists():
        axis_path.write_text(
            "",
            encoding="utf-8",
        )
