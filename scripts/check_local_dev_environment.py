#!/usr/bin/env python3
"""Check local development environment readiness.

Returns a clear PASS/FAIL/WARN report for every required tool and service.
Does not modify anything. Safe to run repeatedly.

Usage:
    python3 scripts/check_local_dev_environment.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _run(cmd: list[str]) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return r.returncode, (r.stdout + r.stderr).strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return 1, ""


def check_python_version() -> tuple[str, str]:
    rc, out = _run([sys.executable, "--version"])
    if rc != 0:
        return "FAIL", "Python not found"
    # e.g. "Python 3.11.9"
    parts = out.split()
    if len(parts) >= 2:
        ver = parts[1]
        major, minor = ver.split(".")[:2]
        if int(major) == 3 and int(minor) == 11:
            return "PASS", f"Python {ver} found"
        return "WARN", f"Python {ver} found (expected 3.11.x)"
    return "WARN", f"Python found: {out}"


def check_node_version() -> tuple[str, str]:
    node = shutil.which("node")
    if not node:
        return "FAIL", "Node not found"
    rc, out = _run(["node", "--version"])
    if rc != 0:
        return "FAIL", "node --version failed"
    # e.g. "v20.11.0"
    ver = out.lstrip("v")
    major = ver.split(".")[0]
    if major == "20":
        return "PASS", f"Node {out} found"
    return "WARN", f"Node {out} found (expected 20.x)"


def check_npm_version() -> tuple[str, str]:
    npm = shutil.which("npm")
    if not npm:
        return "FAIL", "npm not found"
    rc, out = _run(["npm", "--version"])
    if rc != 0:
        return "FAIL", "npm --version failed"
    major = out.split(".")[0]
    if major == "10":
        return "PASS", f"npm {out} found"
    return "WARN", f"npm {out} found (expected 10.x)"


def check_postgres() -> tuple[str, str]:
    pg = shutil.which("psql")
    if not pg:
        return "WARN", "psql not found; Postgres/PostGIS unavailable — use SQLite fallback"
    rc, out = _run(["psql", "--version"])
    if rc == 0:
        return "PASS", f"psql available: {out}"
    return "WARN", f"psql found but --version failed: {out}"


def check_redis() -> tuple[str, str]:
    cli = shutil.which("redis-cli")
    if not cli:
        return "WARN", "redis-cli not found; Redis unavailable — local queue mode only"
    rc, out = _run(["redis-cli", "ping"])
    if rc == 0 and out.strip() == "PONG":
        return "PASS", "Redis available and responding"
    return "WARN", "redis-cli found but server not reachable — local queue mode only"


def check_docker() -> tuple[str, str]:
    docker = shutil.which("docker")
    if not docker:
        return "WARN", "Docker unavailable"
    rc, out = _run(["docker", "info", "--format", "{{.ServerVersion}}"])
    if rc == 0 and out:
        return "PASS", f"Docker available (server {out})"
    return "WARN", "Docker binary found but daemon not running"


def check_frontend_deps() -> tuple[str, str]:
    nm = REPO_ROOT / "frontend" / "node_modules"
    if nm.is_dir():
        return "PASS", "frontend/node_modules present"
    return "WARN", "frontend/node_modules missing — run: cd frontend && npm install"


def check_backend_deps() -> tuple[str, str]:
    venv = REPO_ROOT / "backend" / ".venv"
    site_pkgs = list((REPO_ROOT / "backend").glob(".venv/lib/python*/site-packages"))
    if venv.is_dir() and site_pkgs:
        return "PASS", "backend/.venv present with site-packages"
    # Also check system install
    rc, _ = _run([sys.executable, "-c", "import fastapi"])
    if rc == 0:
        return "PASS", "backend dependencies installed (system Python)"
    return "WARN", "backend/.venv missing — run: cd backend && pip install -e .[dev]"


def check_env_file() -> tuple[str, str]:
    env = REPO_ROOT / ".env"
    if env.is_file():
        return "PASS", ".env file present"
    example = REPO_ROOT / ".env.example"
    if example.is_file():
        return "WARN", ".env missing — copy from .env.example: cp .env.example .env"
    return "FAIL", ".env and .env.example both missing"


def check_evidence_store() -> tuple[str, str]:
    import os

    root = os.environ.get("JTA_EVIDENCE_STORE_ROOT", "")
    if root and Path(root).is_dir():
        return "PASS", f"Evidence store root exists: {root}"
    if root:
        return "WARN", f"JTA_EVIDENCE_STORE_ROOT set to '{root}' but directory missing"
    return "WARN", "JTA_EVIDENCE_STORE_ROOT not set; evidence store unavailable"


CHECKS = [
    ("Python 3.11", check_python_version),
    ("Node 20", check_node_version),
    ("npm 10", check_npm_version),
    ("Postgres/PostGIS", check_postgres),
    ("Redis", check_redis),
    ("Docker", check_docker),
    ("Frontend dependencies", check_frontend_deps),
    ("Backend dependencies", check_backend_deps),
    (".env file", check_env_file),
    ("Evidence store root", check_evidence_store),
]


def main() -> int:
    results: list[tuple[str, str, str]] = []
    for label, fn in CHECKS:
        status, detail = fn()
        results.append((status, label, detail))

    print("\nJUDGE_ATLASX Local Environment Check")
    print("=" * 50)
    for status, label, detail in results:
        print(f"{status:<5} {label}: {detail}")
    print("=" * 50)

    fails = [r for r in results if r[0] == "FAIL"]
    warns = [r for r in results if r[0] == "WARN"]
    passed = [r for r in results if r[0] == "PASS"]

    print(f"\n{len(passed)} PASS  {len(warns)} WARN  {len(fails)} FAIL")
    if fails:
        print("\nFix FAIL items before running the alpha.")
        return 1
    if warns:
        print("\nWARN items are non-blocking but may limit functionality.")
    print("\nEnvironment check complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
