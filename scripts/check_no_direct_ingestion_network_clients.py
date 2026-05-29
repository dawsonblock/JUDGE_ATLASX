#!/usr/bin/env python3
"""Wrapper for check_no_direct_ingestion_network_clients.py

The backend-specific check is located at backend/scripts/ but workflows
reference it from scripts/. This wrapper forwards the call.
"""

from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]
backend_script = ROOT / "backend" / "scripts" / "check_no_direct_ingestion_network_clients.py"

if not backend_script.exists():
    print(f"Error: backend script not found at {backend_script}", file=sys.stderr)
    sys.exit(1)

runpy.run_path(str(backend_script), run_name="__main__")
