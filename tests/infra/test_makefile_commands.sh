#!/usr/bin/env bash
# tests/infra/test_makefile_commands.sh
# Verifies that every Makefile lifecycle target exits with code 0.
# Must be run from the project root.

set -uo pipefail

# Source .env if present
if [ -f .env ]; then
  # shellcheck disable=SC1091
  set -o allexport && source .env && set +o allexport
fi

FAILED=0

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

run_target() {
  local target="$1"
  shift
  local extra_args=("$@")
  local display_name

  if [ "${#extra_args[@]}" -gt 0 ]; then
    display_name="make ${target} ${extra_args[*]}"
  else
    display_name="make ${target}"
  fi

  echo "==> Running: ${display_name}"

  if make "${target}" ${extra_args[@]+"${extra_args[@]}"} 2>&1; then
    echo "PASS: ${display_name} exited 0"
  else
    local code=$?
    echo "FAIL: ${display_name} exited ${code}"
    FAILED=1
  fi
  echo ""
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

# 1. up — bring the stack up (builds images if stale)
run_target up

# 2. ps — show service status (stack must be running)
run_target ps

# 3. logs — no -f flag, so the command returns immediately
run_target logs

# 4. restart — cycle all containers without rebuild
run_target restart

# 5. down — stop containers; volumes must survive (no -v)
run_target down

# ---------------------------------------------------------------------------
# Leave stack running for subsequent tests / developer convenience
# ---------------------------------------------------------------------------
echo "==> Restoring stack to running state (make up)..."
if make up 2>&1; then
  echo "Stack restored."
else
  echo "Warning: could not restore stack after test run."
fi
echo ""

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
if [ "$FAILED" -ne 0 ]; then
  echo "RESULT: One or more Makefile targets failed."
  exit 1
fi

echo "RESULT: All Makefile targets exited 0."
exit 0
