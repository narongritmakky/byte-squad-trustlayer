# Phase 1 — Infrastructure Scaffolding Plan
## byte-squad-trustlayer

---

## Top-Level Overview

**Goal:** Stand up the full project skeleton for the `byte-squad-trustlayer` Trust Layer
system — folder structure, Docker Compose multi-service orchestration, Makefile lifecycle
commands, environment variable template, database init scripts, and documentation stubs —
with no business logic written yet.

**Scope:**
- Folder/file tree for all services and supporting directories
- `docker-compose.yml` covering four services: `db`, `api`, `judge-worker`, `docs-sync`
- `Makefile` wrapping docker compose lifecycle commands
- `.env.example` template
- `db/` PostgreSQL init scripts (pgvector extension only)
- `services/api/`, `services/judge-worker/`, `services/docs-sync/` scaffolds
  (Dockerfile + entrypoint only, no business logic)
- `docs/` stubs mirroring every folder/service
- `tests/infra/` infrastructure checks (defined BEFORE docker-compose and Makefile are
  finalized, per Rule 3)
- Root `README.md` updated to link all docs

**Non-Goals:**
- FastAPI route implementations
- Judge logic or Trust Layer rules
- Custom Bob Modes
- Any application business logic

**Execution Mode:** All sub-tasks run in **Agent Mode**. No Ask Mode consultation is
needed because the repo is a clean slate — all assumptions confirmed by exploration.

---

## Sub-Task 1 — Folder Skeleton and Docs Stubs

**Status:** [x] done

### Intent
Create every directory and placeholder file that Phase 1 requires. Establishing the tree
first gives subsequent sub-tasks a stable target for their file placements and ensures
every folder has a paired doc file (Rule 1).

### Expected Outcomes
- All directories exist under the workspace root
- Every directory has at minimum an empty or stub `README.md` under `docs/`
- A `.gitignore` is present (Python + Docker conventions)

### Todo List
1. Create the following directory tree (use empty `.gitkeep` files where needed to
   commit empty directories):
   ```
   byte-squad-trustlayer/
   ├── .env.example
   ├── .gitignore
   ├── README.md                  (update existing)
   ├── docker-compose.yml         (created in Sub-Task 3)
   ├── Makefile                   (created in Sub-Task 4)
   ├── db/
   │   └── init/
   │       └── 01_enable_pgvector.sql
   ├── services/
   │   ├── api/
   │   │   ├── Dockerfile
   │   │   ├── requirements.txt
   │   │   └── app/
   │   │       └── main.py        (scaffold: FastAPI app object only)
   │   ├── judge-worker/
   │   │   └── worker.py          (scaffold: entry-point loop only)
   │   └── docs-sync/
   │       └── watcher.py         (scaffold: watchdog loop only)
   ├── docs/
   │   ├── architecture.md
   │   ├── db.md
   │   ├── services/
   │   │   ├── api.md
   │   │   ├── judge-worker.md
   │   │   └── docs-sync.md
   │   ├── docker-compose.md
   │   ├── makefile.md
   │   └── tests-infra.md
   ├── tests/
   │   └── infra/
   │       ├── test_containers_start.sh
   │       ├── test_volume_persistence.sh
   │       └── test_makefile_commands.sh
   └── evidence/
       └── (existing screenshots — untouched)
   ```
2. Write `.gitignore` covering: `__pycache__/`, `*.pyc`, `.env`, `.DS_Store`,
   `*.egg-info/`, `dist/`, `.venv/`, `node_modules/`, `*.log`
3. Write stub content for each `docs/*.md` file (title + one-paragraph purpose
   description; no implementation detail yet)
4. Update root `README.md` to include a "Documentation" section linking to every
   `docs/` file and a "Quick Start" section pointing to `make up`

### Relevant Context
- Repo root: `/Volumes/Avertiflow/ibm-bob-project/byte-squad-trustlayer`
- Existing files to preserve: `README.md` (extend), `evidence/` (untouched)

---

## Sub-Task 2 — Infrastructure Tests (defined BEFORE configs, per Rule 3)

**Status:** [x] done

### Intent
Write the three infrastructure check scripts that will be used to validate the Docker
Compose and Makefile output. These must exist before `docker-compose.yml` and the
`Makefile` are finalized so the configs are written to satisfy the tests, not the other
way around.

### Expected Outcomes
- `tests/infra/test_containers_start.sh` — asserts all four containers reach a healthy
  or running state within a timeout
- `tests/infra/test_volume_persistence.sh` — inserts a row into the `db` container,
  runs `make down`, runs `make up`, then queries for the row to confirm it survived
- `tests/infra/test_makefile_commands.sh` — calls each Makefile target (`up`, `down`,
  `restart`, `logs`, `ps`) and asserts exit codes are 0
- All three scripts are executable (`chmod +x`) and produce PASS/FAIL output

### Todo List
1. Write `tests/infra/test_containers_start.sh`:
   - Call `make up` (or `docker compose up -d`)
   - Poll `docker inspect --format='{{.State.Health.Status}}'` for `db` until
     `healthy` or timeout 60 s
   - Poll `docker inspect --format='{{.State.Status}}'` for `api`,
     `judge-worker`, `docs-sync` until `running` or timeout 60 s
   - Print PASS/FAIL per service; exit 1 on any FAIL
2. Write `tests/infra/test_volume_persistence.sh`:
   - Bring stack up (`make up`)
   - Insert a sentinel row: `docker exec <db-container> psql -U $POSTGRES_USER -d $POSTGRES_DB -c "INSERT INTO _infra_test VALUES (1);"`
     (script must create the table first if not exists)
   - Run `make down` (volumes must NOT be removed — only containers)
   - Run `make up`
   - Query row; assert count = 1; print PASS/FAIL
3. Write `tests/infra/test_makefile_commands.sh`:
   - For each target: `up`, `down`, `restart`, `logs --no-follow`, `ps`
   - Run the target; capture exit code
   - Print PASS if exit 0, FAIL otherwise
4. Mark all scripts executable in the same commit
5. Add a note in `docs/tests-infra.md` explaining what each script tests and how to run
   it (`make test-infra` or `bash tests/infra/<script>.sh`)

### Relevant Context
- These scripts are deliberately written BEFORE docker-compose.yml (Sub-Task 3) and
  Makefile (Sub-Task 4) so those artifacts must satisfy the tests
- Variable names (`POSTGRES_USER`, `POSTGRES_DB`) will be sourced from `.env.example`
  conventions; scripts should source a `.env` file if present

---

## Sub-Task 3 — Docker Compose Design

**Status:** [x] done

### Intent
Write `docker-compose.yml` with four services whose design choices are grounded in
maintainability, hot-reload development support, and the health check requirements
surfaced by the infrastructure tests in Sub-Task 2.

### Expected Outcomes
- `docker-compose.yml` is valid (`docker compose config` exits 0)
- `db` service uses the official `pgvector/pgvector:pg16` image; data survives restarts
  via a named volume `pgdata`; health check uses `pg_isready`
- `api` service mounts source code as a volume for hot-reload; `depends_on: db:
  condition: service_healthy`; health check hits `GET /healthz`
- `judge-worker` uses the same image as `api` (built from `services/api/Dockerfile`)
  with a different `command` override; `depends_on: db: condition: service_healthy`
- `docs-sync` is a lightweight Alpine/Python container running the watchdog script;
  depends on nothing; can be restarted independently
- All four services have `restart: unless-stopped` and structured log output

### Todo List

#### Service: db
1. Use image `pgvector/pgvector:pg16` — ships with pgvector pre-compiled; no custom
   build needed
2. Environment variables sourced from `.env` file: `POSTGRES_USER`, `POSTGRES_PASSWORD`,
   `POSTGRES_DB`
3. Named volume: `pgdata:/var/lib/postgresql/data`
4. Health check:
   ```
   test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"]
   interval: 10s
   timeout: 5s
   retries: 5
   ```
5. Mount `./db/init:/docker-entrypoint-initdb.d` so `01_enable_pgvector.sql` runs
   automatically on first boot
6. `restart: unless-stopped`

#### Service: api
1. Build from `./services/api/Dockerfile` (Python 3.12-slim base)
2. Mount `./services/api:/app` for hot-reload (uvicorn `--reload` flag in `command`)
3. Expose port `8000`
4. `depends_on: db: condition: service_healthy`
5. Health check:
   ```
   test: ["CMD-SHELL", "curl -f http://localhost:8000/healthz || exit 1"]
   interval: 15s
   timeout: 5s
   retries: 3
   start_period: 10s
   ```
6. `restart: unless-stopped`

#### Service: judge-worker
1. Build from the same `./services/api/Dockerfile` (shared image, different entrypoint)
2. Override `command: python worker.py` — file lives in the same codebase but runs
   independently; this keeps Dockerfile maintenance to one place
3. Mount `./services/api:/app` (same source tree)
4. `depends_on: db: condition: service_healthy`
5. Health check: simple process check — `test: ["CMD-SHELL", "pgrep -f worker.py || exit 1"]`
6. `restart: unless-stopped`

#### Service: docs-sync
1. Use `python:3.12-alpine` — minimal footprint; only needs watchdog library
2. Build from `./services/docs-sync/Dockerfile` (or inline `build.context`)
3. Mount `./docs:/docs` and `./services/docs-sync:/app`
4. Health check: `test: ["CMD-SHELL", "pgrep -f watcher.py || exit 1"]`
5. `restart: unless-stopped`
6. No `depends_on` — fully independent; can be stopped/started without side effects

#### Top-level
7. Declare named volume `pgdata` at the bottom of the file
8. Add `.env_file: .env` to services that need environment variables
9. Document every design decision in `docs/docker-compose.md`

### Relevant Context
- The infrastructure tests in Sub-Task 2 define the health check shapes; this sub-task
  must satisfy them exactly
- `judge-worker` sharing the `api` Dockerfile is an intentional design choice: single
  source of truth for Python dependencies; divergence only in the `command` override

---

## Sub-Task 4 — Makefile for Project Lifecycle

**Status:** [x] done

### Intent
Write a `Makefile` that wraps the full Docker Compose lifecycle in memorable, single-word
targets so any developer can operate the stack without knowing the underlying docker
compose flags. Targets must satisfy the assertions in `test_makefile_commands.sh`.

### Expected Outcomes
- All seven targets exist and exit 0 when called in a running-stack context
- `make destroy` is the only target that removes volumes
- `make test-infra` runs all three scripts from `tests/infra/`
- The file has a `help` target that self-documents available commands

### Todo List
1. Write the following targets and their exact wrapped commands:

   | Target | Wrapped command | Why |
   |---|---|---|
   | `up` | `docker compose up -d --build` | Builds images if stale; starts detached |
   | `down` | `docker compose down` | Stops containers; volumes survive |
   | `destroy` | `docker compose down -v` | Removes containers AND named volumes |
   | `restart` | `docker compose restart` | Restart without rebuild |
   | `logs` | `docker compose logs -f` | Tails all service logs |
   | `ps` | `docker compose ps` | Shows service status |
   | `test-infra` | `bash tests/infra/test_containers_start.sh && bash tests/infra/test_volume_persistence.sh && bash tests/infra/test_makefile_commands.sh` | Runs all infra checks in order |
   | `help` | `@grep -E '^[a-zA-Z_-]+:' Makefile \| awk ...` | Self-documents targets |

2. Set `.PHONY` for all targets (prevents name collisions with files)
3. Set `COMPOSE_FILE ?= docker-compose.yml` at the top so the file can be overridden
   for CI environments
4. Add a `SHELL := /bin/bash` directive for consistent shell behavior
5. Document the Makefile design and every target in `docs/makefile.md`

### Relevant Context
- `make down` deliberately does NOT use `-v` — volume persistence test in Sub-Task 2
  depends on this distinction
- `make destroy` is the escape hatch for a completely clean environment reset
- `make test-infra` chains scripts with `&&` so it stops on first failure

---

## Sub-Task 5 — Service Scaffolds and DB Init

**Status:** [x] done

### Intent
Write the minimal scaffold files for each service (Dockerfile, entrypoint, requirements)
and the PostgreSQL init SQL. No business logic — only what is needed for the containers
to start, pass health checks, and be overridden in later phases.

### Expected Outcomes
- `services/api/Dockerfile` builds successfully
- `services/api/app/main.py` exposes a single `/healthz` endpoint returning `{"status": "ok"}`
- `services/api/requirements.txt` lists `fastapi`, `uvicorn[standard]`, `psycopg2-binary`
- `services/judge-worker/worker.py` is a minimal infinite loop with a startup log line
- `services/docs-sync/watcher.py` is a minimal watchdog observer pointing at `/docs`
- `db/init/01_enable_pgvector.sql` runs `CREATE EXTENSION IF NOT EXISTS vector;`
- `.env.example` contains all variable names with safe placeholder values

### Todo List
1. Write `db/init/01_enable_pgvector.sql`:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
2. Write `.env.example`:
   ```
   POSTGRES_USER=trustlayer
   POSTGRES_PASSWORD=changeme
   POSTGRES_DB=trustlayer
   DATABASE_URL=postgresql://trustlayer:changeme@db:5432/trustlayer
   ```
3. Write `services/api/requirements.txt`:
   ```
   fastapi
   uvicorn[standard]
   psycopg2-binary
   ```
4. Write `services/api/Dockerfile`:
   - Base: `python:3.12-slim`
   - `WORKDIR /app`
   - `COPY requirements.txt .` → `RUN pip install --no-cache-dir -r requirements.txt`
   - `EXPOSE 8000`
   - `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]`
5. Write `services/api/app/main.py`:
   - Import `FastAPI`; create `app = FastAPI()`
   - Single route: `GET /healthz` → `{"status": "ok"}`
6. Write `services/judge-worker/worker.py`:
   - `import time, logging`
   - Infinite loop: `logging.info("judge-worker: running"); time.sleep(10)`
   - Comment: `# Phase 2: Trust Judge logic will replace this loop`
7. Write `services/docs-sync/watcher.py`:
   - Use `watchdog` library; observe `/docs` directory
   - Log file-change events; sleep loop
   - Comment: `# Phase 2: sync logic will replace this stub`
8. Write `services/docs-sync/Dockerfile`:
   - Base: `python:3.12-alpine`
   - `RUN pip install watchdog`
   - `CMD ["python", "watcher.py"]`
9. Add `watchdog` to a `services/docs-sync/requirements.txt`

### Relevant Context
- The `/healthz` endpoint is the exact path the `api` health check polls in Sub-Task 3
- `worker.py` is the file `judge-worker` service's `command` override references
- No database schema creation happens here — only the pgvector extension; schema is
  Phase 2 responsibility

---

## Sub-Task 6 — Validation Run

**Status:** [x] done

### Intent
Execute the infrastructure tests to confirm all services start, data persists, and
Makefile targets behave correctly. This is the sandbox validation mandated by Rule 2.

### Expected Outcomes
- `make up` completes with no errors
- `docker compose ps` shows all four services healthy/running
- `make test-infra` prints PASS for every check across all three scripts
- `make down` followed by `make up` shows data persisted in `db`
- `make destroy` leaves no containers or volumes behind

### Todo List
1. Copy `.env.example` to `.env` (local only, never committed)
2. Run `make up` and capture output; confirm all four services appear in `docker compose ps`
3. Run `make test-infra`; inspect output line by line; fix any failures before marking
   this sub-task done
4. If any test fails: identify root cause in the relevant config, fix it, and re-run
5. Record passing evidence (terminal output or screenshot) in `evidence/`
6. Update `docs/tests-infra.md` with actual results
7. Mark all sub-tasks done in this plan file

### Relevant Context
- This sub-task runs LAST and depends on Sub-Tasks 1–5 all being complete
- If `test_volume_persistence.sh` fails, the named volume `pgdata` may be misconfigured
  in `docker-compose.yml` — revisit Sub-Task 3
- If `test_containers_start.sh` fails for `api`, the `/healthz` route scaffold in
  Sub-Task 5 is the most likely root cause

---

## Execution Order Summary

```
Sub-Task 1 (Folder Skeleton)
    → Sub-Task 2 (Infra Tests — BEFORE configs)
        → Sub-Task 3 (docker-compose.yml)
            → Sub-Task 4 (Makefile)
                → Sub-Task 5 (Service Scaffolds + DB Init)
                    → Sub-Task 6 (Validation Run)
```

All sub-tasks execute sequentially in **Agent Mode**.
Switch to **Agent Mode** when the user confirms this plan, then process sub-tasks
one at a time using `start_subtask`, reading this file at the start of each sub-task
for full context.
