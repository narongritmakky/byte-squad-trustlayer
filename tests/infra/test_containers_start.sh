#!/usr/bin/env bash
# tests/infra/test_containers_start.sh
# Asserts that all four Docker Compose services reach healthy/running state.
# Must be run from the project root.

set -euo pipefail

# Source .env if present (provides variable context; not required for this script)
if [ -f .env ]; then
  # shellcheck disable=SC1091
  set -o allexport && source .env && set +o allexport
fi

TIMEOUT=60
POLL_INTERVAL=3
FAILED=0

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Poll db container until its health status is "healthy"
wait_healthy() {
  local service="$1"
  local elapsed=0

  echo "Waiting for $service to become healthy (timeout: ${TIMEOUT}s)..."

  while [ "$elapsed" -lt "$TIMEOUT" ]; do
    status=$(docker compose ps -q "$service" | xargs -I{} docker inspect --format='{{.State.Health.Status}}' {} 2>/dev/null || true)
    if [ "$status" = "healthy" ]; then
      echo "PASS: $service is healthy"
      return 0
    fi
    sleep "$POLL_INTERVAL"
    elapsed=$(( elapsed + POLL_INTERVAL ))
  done

  echo "FAIL: $service timed out waiting for healthy (last status: ${status:-unknown})"
  return 1
}

# Poll a container until its run state is "running"
wait_running() {
  local service="$1"
  local elapsed=0

  echo "Waiting for $service to become running (timeout: ${TIMEOUT}s)..."

  while [ "$elapsed" -lt "$TIMEOUT" ]; do
    status=$(docker compose ps -q "$service" | xargs -I{} docker inspect --format='{{.State.Status}}' {} 2>/dev/null || true)
    if [ "$status" = "running" ]; then
      echo "PASS: $service is running"
      return 0
    fi
    sleep "$POLL_INTERVAL"
    elapsed=$(( elapsed + POLL_INTERVAL ))
  done

  echo "FAIL: $service timed out waiting for running (last status: ${status:-unknown})"
  return 1
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

echo "==> Bringing stack up..."
docker compose up -d

wait_healthy "db"           || FAILED=1
wait_running "api"          || FAILED=1
wait_running "judge-worker" || FAILED=1
wait_running "docs-sync"    || FAILED=1

if [ "$FAILED" -ne 0 ]; then
  echo ""
  echo "RESULT: One or more services failed to reach expected state."
  exit 1
fi

echo ""
echo "RESULT: All services are healthy/running."
exit 0
