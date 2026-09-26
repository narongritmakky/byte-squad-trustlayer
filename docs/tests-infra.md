# Infrastructure Tests

Scripts in `tests/infra/` validate the Docker Compose stack and Makefile targets.
Run them individually or all at once via `make test-infra`.

## Validation Results — Sub-Task 6 (2026-09-26)

All three scripts passed after the following fixes were applied:

| Fix | File changed | Root cause |
|---|---|---|
| Added `curl` install to Dockerfile | `services/api/Dockerfile` | Health check uses `curl -f http://localhost:8000/healthz`; `python:3.12-slim` ships without `curl` |
| Changed `judge-worker` health check from `pgrep -f worker.py` to `kill -0 1` | `docker-compose.yml` | `pgrep` not available in `python:3.12-slim` |
| Changed `logs` target to `docker compose logs $(ARGS)` (no hardcoded `-f`) | `Makefile` | `-f` flag causes `make logs` to hang indefinitely |
| Fixed `test_makefile_commands.sh` to call `run_target logs` (no `--no-follow` arg) | `tests/infra/test_makefile_commands.sh` | `docker compose logs` has no `--no-follow` flag; command exits by default without `-f` |
| Fixed `extra_args[@]: unbound variable` crash with `set -u` and empty array | `tests/infra/test_makefile_commands.sh` | Bash `set -u` treats empty arrays as unbound; used `${extra_args[@]+"${extra_args[@]}"}` guard |

### Final `docker compose ps` (post-rebuild after `make destroy`)

```
NAME                                   IMAGE                               SERVICE        STATUS
byte-squad-trustlayer-api-1            byte-squad-trustlayer-api           api            Up (healthy)
byte-squad-trustlayer-db-1             pgvector/pgvector:pg16              db             Up (healthy)
byte-squad-trustlayer-docs-sync-1      byte-squad-trustlayer-docs-sync     docs-sync      Up (healthy)
byte-squad-trustlayer-judge-worker-1   byte-squad-trustlayer-judge-worker  judge-worker   Up (healthy)
```

All four services report `(healthy)`. `make destroy` removed the `byte-squad-trustlayer_pgdata` volume cleanly (exit 0). A subsequent `make up` rebuilt the stack from scratch with all services healthy.

> **Run all three at once**
> ```bash
> make test-infra
> ```
> `make test-infra` chains the scripts with `&&`, so it stops on the first failure.

---

## `test_containers_start.sh`

**What it tests:** All four Docker Compose services reach the expected state within 60 seconds of `docker compose up -d`.

| Service | Expected state | Detection method |
|---|---|---|
| `db` | `healthy` | `docker inspect --format='{{.State.Health.Status}}'` |
| `api` | `running` | `docker inspect --format='{{.State.Status}}'` |
| `judge-worker` | `running` | `docker inspect --format='{{.State.Status}}'` |
| `docs-sync` | `running` | `docker inspect --format='{{.State.Status}}'` |

**Polling:** every 3 seconds; 60-second timeout per service.

**PASS criteria:** Every service reaches its target state before the timeout.  
**FAIL criteria:** Any service exceeds the 60-second timeout. The script prints `FAIL: <service> timed out` for each failure and exits 1.

**Run individually:**
```bash
bash tests/infra/test_containers_start.sh
```

---

## `test_volume_persistence.sh`

**What it tests:** Data written to the `db` container survives a full `docker compose down` / `docker compose up` cycle — confirming the named volume `pgdata` is correctly configured and not destroyed by `down` (which has no `-v` flag).

**Steps performed:**
1. `docker compose up -d`
2. Wait 15 s for the database to accept connections
3. Create table `_infra_test` and insert a sentinel row (`id = 1`)
4. `docker compose down` — containers stop, volume survives
5. `docker compose up -d`
6. Wait 15 s for the database to be ready again
7. `SELECT COUNT(*) FROM _infra_test WHERE id = 1;`

**PASS criteria:** Count equals 1 — the row survived the cycle. Prints `PASS: volume data persisted` and exits 0.  
**FAIL criteria:** Count is not 1 (data was lost or the query errored). Prints `FAIL: data lost after down/up` and exits 1.

> If this test fails, the most likely cause is `docker compose down -v` being used somewhere (which removes named volumes) or the `pgdata` volume not being declared at the top-level `volumes:` section of `docker-compose.yml`.

**Run individually:**
```bash
bash tests/infra/test_volume_persistence.sh
```

---

## `test_makefile_commands.sh`

**What it tests:** Every Makefile lifecycle target completes without error (exit code 0) when called in sequence against a running stack.

**Targets exercised (in order):**

| Target | Equivalent command | Notes |
|---|---|---|
| `make up` | `docker compose up -d --build` | Builds images if stale; starts stack |
| `make ps` | `docker compose ps` | Shows service status |
| `make logs --no-follow` | `docker compose logs --no-follow` | Returns immediately; no tail |
| `make restart` | `docker compose restart` | Cycles all containers without rebuild |
| `make down` | `docker compose down` | Stops containers; volumes survive |

After all targets are exercised, the script runs `make up` once more to leave the stack in a running state for subsequent tests or developer use.

**PASS criteria:** Every target exits 0. Prints `PASS: make <target> exited 0` per target and exits 0.  
**FAIL criteria:** Any target exits non-zero. Prints `FAIL: make <target> exited <code>` and exits 1 at the end of the run (all targets still execute so all failures are reported together).

**Run individually:**
```bash
bash tests/infra/test_makefile_commands.sh
```

---

## Environment variables

Scripts source `.env` from the project root if the file exists:

```bash
# .env is auto-sourced when present
POSTGRES_USER=trustlayer
POSTGRES_DB=trustlayer
```

If `.env` is absent, `test_volume_persistence.sh` falls back to the `.env.example` defaults (`trustlayer`/`trustlayer`). Copy `.env.example` to `.env` before running:

```bash
cp .env.example .env
```

---

## PASS/FAIL summary

| Script | PASS condition | FAIL condition | Exit on first failure? |
|---|---|---|---|
| `test_containers_start.sh` | All 4 services reach expected state ≤ 60 s | Any service times out | No — checks all, reports all |
| `test_volume_persistence.sh` | Sentinel row count = 1 after down/up | Count ≠ 1 or query errors | Yes (single assertion) |
| `test_makefile_commands.sh` | All targets exit 0 | Any target exits non-zero | No — runs all targets, reports all |
