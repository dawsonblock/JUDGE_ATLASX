#!/usr/bin/env bash
set -euo pipefail

# Docker Compose smoke proof for Judge Atlas
# Usage: ./scripts/proof_docker_compose.sh
# Set KEEP_STACK=1 to preserve containers after test

KEEP_STACK="${KEEP_STACK:-0}"
COMPOSE_FILE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/../docker-compose.yml"
JTA_BACKEND_PORT="${JTA_BACKEND_PORT:-8000}"
JTA_FRONTEND_PORT="${JTA_FRONTEND_PORT:-3000}"
JTA_DB_PORT="${JTA_DB_PORT:-5432}"
JTA_REDIS_PORT="${JTA_REDIS_PORT:-6379}"
JTA_MINIO_PORT="${JTA_MINIO_PORT:-9000}"
JTA_MINIO_CONSOLE_PORT="${JTA_MINIO_CONSOLE_PORT:-9001}"
export JTA_BACKEND_PORT JTA_FRONTEND_PORT JTA_DB_PORT
export JTA_REDIS_PORT JTA_MINIO_PORT JTA_MINIO_CONSOLE_PORT

# Provide test-only placeholder tokens so CI/proof runs don't require a .env file
export JTA_ADMIN_TOKEN="${JTA_ADMIN_TOKEN:-proof-admin-token-ci}"
export JTA_ADMIN_REVIEW_TOKEN="${JTA_ADMIN_REVIEW_TOKEN:-proof-review-token-ci}"

log() { echo "[proof_docker] $*"; }

dump_diagnostics() {
    log "Diagnostics: docker compose version"
    docker compose version || true
    log "Diagnostics: docker compose config"
    docker compose -f "$COMPOSE_FILE" config || true
    log "Diagnostics: docker compose ps"
    docker compose -f "$COMPOSE_FILE" ps || true
    log "Diagnostics: backend logs"
    docker compose -f "$COMPOSE_FILE" logs backend || true
    log "Diagnostics: frontend logs"
    docker compose -f "$COMPOSE_FILE" logs frontend || true
    log "Diagnostics: db logs"
    docker compose -f "$COMPOSE_FILE" logs db || true
}

cleanup() {
    if [ "$KEEP_STACK" != "1" ]; then
        log "Tearing down stack..."
        docker compose -f "$COMPOSE_FILE" down -v 2>/dev/null || true
    fi
}
trap cleanup EXIT

log "Step 1: Tearing down any existing stack..."
docker compose -f "$COMPOSE_FILE" down -v 2>/dev/null || true

log "Step 2: Building images..."
docker compose version
docker compose -f "$COMPOSE_FILE" build

log "Step 3: Starting stack..."
docker compose -f "$COMPOSE_FILE" up -d

log "Step 4: Waiting for backend health..."
for i in $(seq 1 60); do
    if curl -sf "http://localhost:${JTA_BACKEND_PORT}/health" > /dev/null 2>&1; then
        log "Backend ready after ${i}s"
        break
    fi
    if [ "$i" -eq 60 ]; then
        log "ERROR: Backend not ready after 60s"
        dump_diagnostics
        exit 1
    fi
    sleep 1
done

log "Step 5: Checking /health endpoint..."
curl -sv "http://localhost:${JTA_BACKEND_PORT}/health" | head -100

log "Step 6: Checking /api/map/events endpoint..."
map_payload="$(curl -sf "http://localhost:${JTA_BACKEND_PORT}/api/map/events?bbox=-180,-90,180,90")" || {
    log "ERROR: map events endpoint check failed"
    dump_diagnostics
    exit 1
}
printf '%s\n' "$map_payload" | head -200

printf '%s' "$map_payload" | python3 -c 'import json,sys;json.load(sys.stdin)' >/dev/null || {
    log "ERROR: map events endpoint did not return valid JSON"
    dump_diagnostics
    exit 1
}

log "Step 7: Checking frontend root..."
curl -sf "http://localhost:${JTA_FRONTEND_PORT}/" > /dev/null && log "Frontend root: OK" || {
    log "ERROR: Frontend not reachable"
    dump_diagnostics
    exit 1
}

log "SUCCESS: Docker Compose smoke proof passed"
