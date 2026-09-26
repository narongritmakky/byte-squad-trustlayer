#!/usr/bin/env bash
# tests/infra/test_volume_persistence.sh
# Confirms that named Docker volume data survives a `docker compose down` / `up` cycle.
# Must be run from the project root.

set -euo pipefail

# Source .env if present — needed for POSTGRES_USER and POSTGRES_DB
if [ -f .env ]; then
  # shellcheck disable=SC1091
  set -o allexport && source .env && set +o allexport
fi

# Fallback defaults matching .env.example
POSTGRES_USER="${POSTGRES_USER:-trustlayer}"
POSTGRES_DB="${POSTGRES_DB:-trustlayer}"

DB_READY_WAIT=15   # seconds to wait for db to accept connections

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

run_sql() {
  docker compose exec -T db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "$1"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

echo "==> Bringing stack up..."
docker compose up -d

echo "==> Waiting ${DB_READY_WAIT}s for db to be ready..."
sleep "$DB_READY_WAIT"

echo "==> Creating test table and inserting sentinel row..."
run_sql "CREATE TABLE IF NOT EXISTS _infra_test (id INTEGER);"
run_sql "DELETE FROM _infra_test;"          # idempotent: clear any previous run
run_sql "INSERT INTO _infra_test VALUES (1);"

echo "==> Running docker compose down (volumes preserved)..."
docker compose down

echo "==> Bringing stack back up..."
docker compose up -d

echo "==> Waiting ${DB_READY_WAIT}s for db to be ready again..."
sleep "$DB_READY_WAIT"

echo "==> Querying for sentinel row..."
# psql -t: tuples only; -A: unaligned; strip whitespace
COUNT=$(run_sql "SELECT COUNT(*) FROM _infra_test WHERE id = 1;" | grep -E '^\s*[0-9]+\s*$' | tr -d ' ' || echo "0")

echo "Row count returned: ${COUNT}"

if [ "$COUNT" = "1" ]; then
  echo "PASS: volume data persisted"
  exit 0
else
  echo "FAIL: data lost after down/up (expected 1 row, got ${COUNT})"
  exit 1
fi
