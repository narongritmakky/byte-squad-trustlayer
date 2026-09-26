# Byte Squad TrustLayer

A multi-service Trust Layer platform built with FastAPI, PostgreSQL + pgvector, and Docker Compose.

## Quick Start

```bash
cp .env.example .env
make up
```

The stack starts four services: `db`, `api`, `judge-worker`, and `docs-sync`. Run `make help` to see all available lifecycle commands.

## Documentation

| Document | Description |
|---|---|
| [Architecture](docs/architecture.md) | High-level system overview and service relationships |
| [Database](docs/db.md) | PostgreSQL + pgvector setup, volumes, and init scripts |
| [API Service](docs/services/api.md) | FastAPI service, health check, and hot-reload setup |
| [Judge Worker](docs/services/judge-worker.md) | Async Trust Judge worker service |
| [Docs-Sync](docs/services/docs-sync.md) | Watchdog-based documentation sync service |
| [Docker Compose](docs/docker-compose.md) | Service orchestration, health checks, and config |
| [Makefile](docs/makefile.md) | Lifecycle targets and usage |
| [Infrastructure Tests](docs/tests-infra.md) | Validation scripts and how to run them |
