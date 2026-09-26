# Docker Compose

This document explains every design decision in `docker-compose.yml`, which orchestrates the four TrustLayer services: `db`, `api`, `judge-worker`, and `docs-sync`.

---

## Services

### `db`

**Image:** `pgvector/pgvector:pg16`

The official pgvector image ships with the `vector` extension pre-compiled against PostgreSQL 16. No custom Dockerfile is needed — the extension is already installed inside the image. The `db/init/01_enable_pgvector.sql` init script only has to run `CREATE EXTENSION IF NOT EXISTS vector;` rather than compile anything.

**Health check:**

```yaml
test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"]
interval: 10s
timeout: 5s
retries: 5
start_period: 10s
```

`pg_isready` is the canonical liveness probe bundled in every PostgreSQL image. The `$$` double-dollar escaping is required by Docker Compose to pass a literal `$` into the shell (the outer layer would otherwise try to expand `$POSTGRES_USER` at compose parse time). The `start_period: 10s` gives PostgreSQL time to initialise its data directory on first boot before the retry counter starts.

`api` and `judge-worker` carry `depends_on: db: condition: service_healthy`, so they will not start until this health check passes.

---

### `api`

**Build:** `./services/api` (Python 3.12-slim base)

The API service is built from a local Dockerfile rather than a pre-built image. This keeps the build reproducible and lets the team pin Python dependencies in `services/api/requirements.txt`.

**Hot-reload:**

```yaml
volumes:
  - ./services/api:/app
command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The entire `services/api/` source tree is bind-mounted into `/app` inside the container. Combined with uvicorn's `--reload` flag, any file saved on the host is immediately reflected inside the running container — no rebuild required. In production the bind mount would be removed and the code baked into the image at build time.

**Health check:**

```yaml
test: ["CMD-SHELL", "curl -f http://localhost:8000/healthz || exit 1"]
interval: 15s
timeout: 5s
retries: 3
start_period: 15s
```

`curl -f` returns a non-zero exit code on any HTTP error response, making it a reliable probe. The `/healthz` route in `services/api/app/main.py` returns `{"status": "ok"}` as soon as uvicorn is accepting connections. `start_period: 15s` accounts for the time uvicorn takes to import the application on a cold start.

---

### `judge-worker`

**Build:** `./services/api` (same Dockerfile as `api`)

The judge-worker shares the `api` Dockerfile intentionally. Both services are Python processes that talk to the same database using the same set of libraries (`fastapi`, `uvicorn`, `psycopg2-binary`). A single Dockerfile means a single place to update dependencies — there is no risk of `api` and `judge-worker` drifting onto different library versions.

The only difference between the two services is the `command` override:

```yaml
command: python /app/judge-worker/worker.py
```

**Volume strategy:**

```yaml
volumes:
  - ./services/api:/app                        # shared Python environment
  - ./services/judge-worker:/app/judge-worker  # worker source code
```

`worker.py` lives in `services/judge-worker/` on the host (its own directory, separate from the FastAPI application code). The second bind mount injects it into the container at `/app/judge-worker/` so the command `python /app/judge-worker/worker.py` resolves correctly. This avoids duplicating `worker.py` into `services/api/` and keeps the two services' source trees independent.

**Health check:**

```yaml
test: ["CMD-SHELL", "pgrep -f worker.py || exit 1"]
interval: 15s
timeout: 5s
retries: 3
start_period: 10s
```

`pgrep -f` scans the full command line of every process and succeeds as long as one process whose invocation string contains `worker.py` is alive. This is the appropriate probe for a long-running background worker that does not expose an HTTP port.

---

### `docs-sync`

**Build:** `./services/docs-sync` (Python 3.12-alpine base)

`docs-sync` is a lightweight watchdog process that monitors the `docs/` directory. Alpine keeps the image minimal — the only runtime dependency is the `watchdog` Python library.

**No `depends_on`:** `docs-sync` is fully independent of the database and API. It can be stopped, started, or restarted without any effect on the rest of the stack.

**Volume strategy:**

```yaml
volumes:
  - ./docs:/docs               # watched directory
  - ./services/docs-sync:/app  # watcher source (hot-reload friendly)
working_dir: /app
command: python watcher.py
```

`./docs` is mounted read-write at `/docs` so the watcher can both observe and, in a later phase, write back processed output. The `services/docs-sync` source directory is mounted at `/app` for the same hot-reload benefit the `api` service enjoys.

**Health check:**

```yaml
test: ["CMD-SHELL", "pgrep -f watcher.py || exit 1"]
```

Same `pgrep -f` pattern as `judge-worker` — appropriate for a process with no HTTP endpoint.

---

## Volume Strategy

| Volume | Type | Purpose |
|---|---|---|
| `pgdata` | Named volume | Persists PostgreSQL data across `docker compose down` / `up` cycles. Named volumes are managed by Docker and survive container removal. Only `docker compose down -v` (i.e., `make destroy`) removes them. |
| `./db/init` → `/docker-entrypoint-initdb.d` | Bind mount (ro) | Seeds the database on first boot. Read-only prevents the container from writing back to the host init directory. |
| `./services/api` → `/app` | Bind mount | Hot-reload source for `api` and `judge-worker`. Changes on the host are immediately visible inside the container. |
| `./services/judge-worker` → `/app/judge-worker` | Bind mount | Injects the worker script into the shared `api` container image at a known path without coupling the two source directories. |
| `./docs` → `/docs` | Bind mount | Gives `docs-sync` visibility of all documentation files on the host. |
| `./services/docs-sync` → `/app` | Bind mount | Hot-reload source for the docs watcher. |

---

## Environment Variables

All services that need database credentials use `env_file: .env`. This file is never committed to source control (it is in `.gitignore`). Copy `.env.example` to `.env` before starting the stack:

```bash
cp .env.example .env
```

The `.env` file must define at minimum:

```
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_DB=...
DATABASE_URL=postgresql://<user>:<password>@db:5432/<db>
```

`docs-sync` does not need database credentials and therefore has no `env_file`.

---

## Startup Order

```
db  ──(service_healthy)──▶  api
                        ──▶  judge-worker

docs-sync  (no dependency — starts immediately)
```

Docker Compose waits for `db`'s `pg_isready` health check to pass before it starts `api` or `judge-worker`. This prevents the Python services from attempting database connections before PostgreSQL is ready to accept them.
