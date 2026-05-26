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

    if command -v setsid >/dev/null 2>&1; then
        setsid "$@" &
    else
        "$@" &
    fi
    local cmd_pid="$!"

    (
        sleep "$timeout_seconds"
        kill -TERM "-$cmd_pid" 2>/dev/null || kill -TERM "$cmd_pid" 2>/dev/null || exit 0
        sleep 1
        kill -KILL "-$cmd_pid" 2>/dev/null || kill -KILL "$cmd_pid" 2>/dev/null || true
    ) &
    local watchdog_pid="$!"

    local cmd_rc=0
    if ! wait "$cmd_pid"; then
        cmd_rc="$?"
    fi

    kill "$watchdog_pid" 2>/dev/null || true
    wait "$watchdog_pid" 2>/dev/null || true

    if [ "$cmd_rc" -eq 143 ] || [ "$cmd_rc" -eq 137 ]; then
        return 142
    fi
    return "$cmd_rc"
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

    if [ "$rc" -eq 124 ] || [ "$rc" -eq 142 ]; then
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

echo "[docker_runtime] Running docker --version (client)..."
if ! docker --version; then
    echo "[docker_runtime] FAIL_CLASS=DOCKER_GENERIC_FAILURE"
    echo "[docker_runtime] FAIL: docker --version failed"
    exit 1
fi

echo "[docker_runtime] Running docker context ls..."
if ! docker context ls; then
    echo "[docker_runtime] FAIL_CLASS=DOCKER_GENERIC_FAILURE"
    echo "[docker_runtime] FAIL: docker context ls failed"
    exit 1
fi

echo "[docker_runtime] Resolving active Docker context endpoint..."
CURRENT_CONTEXT="$(docker context show 2>/dev/null || true)"
if [ -z "$CURRENT_CONTEXT" ]; then
    echo "[docker_runtime] FAIL_CLASS=DOCKER_GENERIC_FAILURE"
    echo "[docker_runtime] FAIL: unable to resolve active docker context"
    exit 1
fi

DOCKER_ENDPOINT="$(docker context inspect "$CURRENT_CONTEXT" --format '{{(index .Endpoints "docker").Host}}' 2>/dev/null || true)"
if [ -z "$DOCKER_ENDPOINT" ]; then
    echo "[docker_runtime] FAIL_CLASS=DOCKER_GENERIC_FAILURE"
    echo "[docker_runtime] FAIL: unable to resolve docker endpoint for context ${CURRENT_CONTEXT}"
    exit 1
fi
echo "[docker_runtime] INFO: active_context=${CURRENT_CONTEXT}"
echo "[docker_runtime] INFO: docker_endpoint=${DOCKER_ENDPOINT}"

if [[ "$DOCKER_ENDPOINT" == unix://* ]]; then
    DOCKER_SOCK_PATH="${DOCKER_ENDPOINT#unix://}"
    if [ ! -S "$DOCKER_SOCK_PATH" ]; then
        echo "[docker_runtime] FAIL_CLASS=DOCKER_DAEMON_UNAVAILABLE"
        echo "[docker_runtime] FAIL: docker daemon socket not found at ${DOCKER_SOCK_PATH}"
        echo "[docker_runtime] HINT: start Docker Desktop and retry once daemon is healthy"
        exit 1
    fi

    if ! python3 - "$DOCKER_SOCK_PATH" <<'PY'
import socket
import sys

sock_path = sys.argv[1]
client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.settimeout(3)
try:
    client.connect(sock_path)
    client.sendall(b"GET /_ping HTTP/1.1\r\nHost: docker\r\nConnection: close\r\n\r\n")
    payload = client.recv(256)
    if b"OK" not in payload and b"200" not in payload:
        raise RuntimeError("daemon ping did not return OK")
finally:
    client.close()
PY
    then
        echo "[docker_runtime] FAIL_CLASS=DOCKER_DAEMON_UNAVAILABLE"
        echo "[docker_runtime] FAIL: docker daemon socket is present but not responding"
        echo "[docker_runtime] HINT: restart Docker Desktop and verify daemon health"
        exit 1
    fi
elif [[ "$DOCKER_ENDPOINT" == tcp://* ]]; then
    echo "[docker_runtime] INFO: tcp docker endpoint detected; skipping unix socket probe"
else
    echo "[docker_runtime] FAIL_CLASS=DOCKER_GENERIC_FAILURE"
    echo "[docker_runtime] FAIL: unsupported docker endpoint scheme: ${DOCKER_ENDPOINT}"
    exit 1
fi
echo "[docker_runtime] PASS: docker daemon reachable"

echo "[docker_runtime] Checking postgis image metadata..."
if run_with_timeout "$DOCKER_TIMEOUT_SECONDS" docker image inspect postgis/postgis:16-3.4 >/dev/null 2>&1; then
    echo "[docker_runtime] PASS: postgis image present locally"
else
    echo "[docker_runtime] INFO: postgis image not found locally"
fi

echo "[docker_runtime] SUCCESS: Docker runtime preflight completed"
