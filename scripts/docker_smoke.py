#!/usr/bin/env python3
"""Docker smoke checks for local release gating.

Writes canonical output to .validation_logs/docker_smoke.log.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = REPO_ROOT / ".validation_logs"
LOG_PATH = LOG_DIR / "docker_smoke.log"


class SmokeError(RuntimeError):
    pass


def _log(lines: list[str]) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _run(
    lines: list[str],
    cmd: list[str],
    *,
    timeout: int,
    allow_failure: bool = False,
) -> subprocess.CompletedProcess[str]:
    lines.append(f"$ {' '.join(cmd)}")
    cp = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
    )
    output = ((cp.stdout or "") + (cp.stderr or "")).strip()
    if output:
        lines.append(output)
    if cp.returncode != 0 and not allow_failure:
        raise SmokeError(f"command_failed:{' '.join(cmd)}:rc={cp.returncode}")
    return cp


def _append_logs(lines: list[str], service: str) -> None:
    try:
        cp = subprocess.run(
            ["docker", "compose", "logs", service, "--tail", "200"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
    except Exception as exc:  # pragma: no cover - defensive logging path
        lines.append(f"log_capture_error:{service}:{exc}")
        return
    lines.append(f"--- {service} logs (tail 200) ---")
    if cp.stdout:
        lines.append(cp.stdout.rstrip())
    if cp.stderr:
        lines.append(cp.stderr.rstrip())


def _wait_http(lines: list[str], url: str, attempts: int, timeout: int) -> bool:
    for attempt in range(1, attempts + 1):
        cp = subprocess.run(
            ["curl", "-fsS", url],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
        if cp.returncode == 0:
            lines.append(f"http_ready:{url}:attempt={attempt}")
            return True
    return False


def main() -> int:
    lines: list[str] = ["docker smoke", f"repo_root: {REPO_ROOT}"]
    failed = False

    try:
        _run(lines, ["docker", "compose", "down", "-v"], timeout=120, allow_failure=True)

        _run(lines, ["docker", "compose", "build", "--no-cache"], timeout=1800)
        lines.append("docker compose build: PASS")

        _run(lines, ["docker", "compose", "up", "-d", "db", "redis", "minio"], timeout=300)

        # Postgres (db service)
        _run(
            lines,
            [
                "docker",
                "compose",
                "exec",
                "-T",
                "db",
                "pg_isready",
                "-U",
                "judgetracker",
                "-d",
                "judgetracker",
            ],
            timeout=30,
        )
        lines.append("postgres health: PASS")

        # Redis
        redis_ok = False
        for _ in range(20):
            cp = _run(
                lines,
                ["docker", "compose", "exec", "-T", "redis", "redis-cli", "ping"],
                timeout=20,
                allow_failure=True,
            )
            if "PONG" in ((cp.stdout or "") + (cp.stderr or "")):
                redis_ok = True
                break
        if not redis_ok:
            raise SmokeError("redis_not_healthy")
        lines.append("redis health: PASS")

        # MinIO
        if not _wait_http(lines, "http://localhost:9000/minio/health/live", attempts=30, timeout=5):
            raise SmokeError("minio_not_healthy")
        lines.append("minio health: PASS")

        _run(lines, ["docker", "compose", "up", "-d", "backend"], timeout=300)

        backend_ready = _wait_http(lines, "http://localhost:8000/health", attempts=40, timeout=5)
        if not backend_ready:
            backend_ready = _wait_http(lines, "http://localhost:8000/api/health", attempts=10, timeout=5)
        if not backend_ready:
            raise SmokeError("backend_health_endpoint_failed")
        lines.append("backend health: PASS")

        # Verify migrations are healthy in container
        cp = _run(
            lines,
            ["docker", "compose", "exec", "-T", "backend", "alembic", "heads"],
            timeout=60,
            allow_failure=True,
        )
        heads_output = ((cp.stdout or "") + (cp.stderr or "")).lower()
        if cp.returncode != 0:
            raise SmokeError("backend_alembic_heads_failed")
        if "head" not in heads_output:
            raise SmokeError("backend_alembic_heads_missing")

        _run(lines, ["docker", "compose", "up", "-d", "frontend"], timeout=300)
        if not _wait_http(lines, "http://localhost:3000", attempts=40, timeout=5):
            raise SmokeError("frontend_http_failed")

        # Frontend -> backend reachability from container using node runtime.
        cp = _run(
            lines,
            [
                "docker",
                "compose",
                "exec",
                "-T",
                "frontend",
                "node",
                "-e",
                (
                    "const http=require('http');"
                    "http.get('http://backend:8000/health',res=>{"
                    "if(res.statusCode>=200&&res.statusCode<400){process.exit(0);}"
                    "process.exit(1);"
                    "}).on('error',()=>process.exit(1));"
                ),
            ],
            timeout=30,
            allow_failure=True,
        )
        if cp.returncode != 0:
            raise SmokeError("frontend_cannot_reach_backend")
        lines.append("frontend health: PASS")

        lines.append("docker smoke: PASS")
        _run(lines, ["docker", "compose", "down", "-v"], timeout=180, allow_failure=True)
        _log(lines)
        return 0

    except SmokeError as exc:
        failed = True
        lines.append(f"docker smoke failure: {exc}")
        for service in ("db", "redis", "minio", "backend", "frontend"):
            _append_logs(lines, service)
    except subprocess.TimeoutExpired as exc:
        failed = True
        lines.append(f"docker smoke timeout: {exc}")
        for service in ("db", "redis", "minio", "backend", "frontend"):
            _append_logs(lines, service)
    finally:
        try:
            _run(lines, ["docker", "compose", "down", "-v"], timeout=180, allow_failure=True)
        except Exception:
            lines.append("docker compose down -v failed during cleanup")
        lines.append("docker smoke: FAIL" if failed else "docker smoke: PASS")
        _log(lines)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
