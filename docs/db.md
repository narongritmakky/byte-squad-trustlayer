# Database

The `db` service runs a PostgreSQL 16 instance with the `pgvector` extension pre-compiled via the official `pgvector/pgvector:pg16` image.

---

## Files

| Path | Purpose |
|---|---|
| `db/init/01_enable_pgvector.sql` | Runs automatically on first container boot; executes `CREATE EXTENSION IF NOT EXISTS vector;` to activate the pgvector extension |

---

## How the init script runs

Docker's official PostgreSQL image executes every `*.sql` file found in `/docker-entrypoint-initdb.d/` on first boot (i.e. when the data volume is empty). The `docker-compose.yml` bind-mounts `./db/init` to that path, so `01_enable_pgvector.sql` is picked up automatically — no manual step required.

---

## Running locally

```bash
make up        # starts all four services including db
make ps        # confirm db is healthy
make down      # stop containers; named volume pgdata is preserved
make destroy   # stop containers AND remove the pgdata volume (full reset)
```

The `db` service must reach a `healthy` state (via `pg_isready`) before `api` and `judge-worker` start. This is enforced by the `depends_on: condition: service_healthy` clauses in `docker-compose.yml`.

---

## Environment variables

| Variable | Default (`.env.example`) | Description |
|---|---|---|
| `POSTGRES_USER` | `trustlayer` | PostgreSQL superuser name |
| `POSTGRES_PASSWORD` | `changeme` | PostgreSQL superuser password |
| `POSTGRES_DB` | `trustlayer` | Default database name |
| `DATABASE_URL` | `postgresql://trustlayer:changeme@db:5432/trustlayer` | Full connection string for application services |

Copy `.env.example` to `.env` before running:

```bash
cp .env.example .env
```

> **Note:** `.env` is listed in `.gitignore` and must never be committed.

---

## Data persistence

Data is stored in the named Docker volume `pgdata`. The volume survives `make down` and is only removed by `make destroy`. Schema migrations are a Phase 2 responsibility; no application tables are created in this scaffold.
