#!/usr/bin/env bash
set -euo pipefail

# Preflight Docker runtime diagnostics for proof gating.
# This script is intentionally fast-failing so release_gate can report
# environment blockers before PostGIS setup begins.

DOCKER_TIMEOUT_SECONDS="${JTA_DOCKER_CHECK_TIMEOUT:-180}"
if ! [[ "$DOCKER_TIMEOUT_SECONDS" =~ ^[0-9]+$ ]]; then
    DOCKER_TIMEOUT_SECONDS=180
fi
if [ "$DOCKER_TIMEOUT_SECONDS" -lt 60 ]; then
    echo "[docker_runtime] INFO: clamping timeout to 60s (requested ${DOCKER_TIMEOUT_SECONDS}s)"
    DOCKER_TIMEOUT_SECONDS=60
fi

run_with_timeout() {
    local timeout_seconds="$1"
    shift

    python3 - "$timeout_seconds" "$@" <<'PY'
import subprocess
import sys

timeout_seconds = int(sys.argv[1])
command = sys.argv[2:]

try:
    proc = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        check=False,
    )
except subprocess.TimeoutExpired as exc:
    if exc.stdout:
        print(exc.stdout, end="")
    if exc.stderr:
        print(exc.stderr, end="", file=sys.stderr)
    joined = " ".join(command)
    print(
        "[docker_runtime] ERROR: command timed out "
        f"after {timeout_seconds}s: {joined}",
        file=sys.stderr,
    )
    sys.exit(124)

if proc.stdout:
    print(proc.stdout, end="")
if proc.stderr:
    print(proc.stderr, end="", file=sys.stderr)
sys.exit(proc.returncode)
PY
}

classify_docker_failure() {
    local output="$1"
    if printf '%s' "$output" | grep -Eiq 'timed out|context deadline exceeded|deadline exceeded'; then
        echo "DOCKER_TIMEOUT"
        return
    fi
    if printf '%s' "$output" | grep -Eiq 'permission denied.*docker\.sock|got permission denied while trying to connect to the docker daemon socket'; then
        echo "DOCKER_PERMISSION_DENIED"
        return
    fi
    if printf '%s' "$output" | grep -Eiq 'cannot connect to the docker daemon|is the docker daemon running|error during connect|docker desktop.*(not running|stopped)|cannot connect to the docker daemon at'; then
        echo "DOCKER_DAEMON_UNAVAILABLE"
        return
    fi
    echo "DOCKER_GENERIC_FAILURE"
}

run_docker_check() {
    local label="$1"
    shift

    local rc output
    set +e
    output="$(run_with_timeout "$DOCKER_TIMEOUT_SECONDS" "$@" 2>&1)"
    rc="$?"
    set -e
    printf '%s\n' "$output"

    if [ "$rc" -eq 0 ]; then
        echo "[docker_runtime] PASS: ${label} completed"
        return 0
    fi

    if [ "$rc" -eq 124 ]; then
        echo "[docker_runtime] FAIL_CLASS=DOCKER_TIMEOUT"
        echo "[docker_runtime] FAIL: ${label} timed out after ${DOCKER_TIMEOUT_SECONDS}s"
        echo "[docker_runtime] HINT: start Docker Desktop or verify Docker daemon/socket access"
        echo "[docker_runtime] HINT: increase timeout with JTA_DOCKER_CHECK_TIMEOUT if daemon cold-start is slow"
        return 1
    fi

    case "$(classify_docker_failure "$output")" in
        DOCKER_PERMISSION_DENIED)
            echo "[docker_runtime] FAIL_CLASS=DOCKER_PERMISSION_DENIED"
            echo "[docker_runtime] FAIL: permission denied while accessing Docker daemon/socket"
            echo "[docker_runtime] HINT: verify user access to Docker socket and that Docker Desktop is running"
            ;;
        DOCKER_DAEMON_UNAVAILABLE)
            echo "[docker_runtime] FAIL_CLASS=DOCKER_DAEMON_UNAVAILABLE"
            echo "[docker_runtime] FAIL: docker daemon unavailable"
            echo "[docker_runtime] HINT: start Docker Desktop and retry once daemon is healthy"
            ;;
        DOCKER_TIMEOUT)
            echo "[docker_runtime] FAIL_CLASS=DOCKER_TIMEOUT"
            echo "[docker_runtime] FAIL: ${label} timed out after ${DOCKER_TIMEOUT_SECONDS}s"
            echo "[docker_runtime] HINT: daemon may be cold-starting or unresponsive"
            ;;
        *)
            echo "[docker_runtime] FAIL_CLASS=DOCKER_GENERIC_FAILURE"
            echo "[docker_runtime] FAIL: ${label} failed"
            echo "[docker_runtime] HINT: inspect docker diagnostics and local daemon configuration"
            ;;
    esac
    return 1
}

echo "[docker_runtime] Checking docker CLI availability..."
if ! command -v docker >/dev/null 2>&1; then
    echo "[docker_runtime] FAIL_CLASS=DOCKER_CLI_MISSING"
    echo "[docker_runtime] FAIL: docker command not found"
    echo "[docker_runtime] HINT: install Docker CLI and ensure it is on PATH"
    exit 1
fi
echo "[docker_runtime] PASS: docker CLI found: $(command -v docker)"
echo "[docker_runtime] INFO: timeout=${DOCKER_TIMEOUT_SECONDS}s"
echo "[docker_runtime] INFO: user=$(id -un) uid=$(id -u)"

echo "[docker_runtime] Running docker --version..."
if ! run_with_timeout "$DOCKER_TIMEOUT_SECONDS" docker --version; then
    echo "[docker_runtime] FAIL_CLASS=DOCKER_GENERIC_FAILURE"
    echo "[docker_runtime] FAIL: docker --version failed"
    exit 1
fi

echo "[docker_runtime] Running docker context ls..."
if ! run_with_timeout "$DOCKER_TIMEOUT_SECONDS" docker context ls; then
    echo "[docker_runtime] FAIL_CLASS=DOCKER_GENERIC_FAILURE"
    echo "[docker_runtime] FAIL: docker context ls failed"
    exit 1
fi

echo "[docker_runtime] Running docker compose version..."
if ! run_with_timeout "$DOCKER_TIMEOUT_SECONDS" docker compose version; then
    echo "[docker_runtime] FAIL_CLASS=DOCKER_GENERIC_FAILURE"
    echo "[docker_runtime] FAIL: docker compose version failed"
    exit 1
fi

echo "[docker_runtime] Running docker version..."
if ! run_docker_check "docker version" docker version; then
    exit 1
fi
echo "[docker_runtime] PASS: docker version completed"

echo "[docker_runtime] Running docker info..."
if ! run_docker_check "docker info" docker info; then
    exit 1
fi
echo "[docker_runtime] PASS: docker daemon reachable"
echo "[docker_runtime] PASS: docker info completed"

echo "[docker_runtime] Checking postgis image metadata..."
if run_with_timeout "$DOCKER_TIMEOUT_SECONDS" docker image inspect postgis/postgis:16-3.4 >/dev/null 2>&1; then
    echo "[docker_runtime] PASS: postgis image present locally"
else
    echo "[docker_runtime] INFO: postgis image not found locally"
fi

echo "[docker_runtime] SUCCESS: Docker runtime preflight completed"
