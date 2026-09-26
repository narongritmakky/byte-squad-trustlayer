# Judge Worker Service

The `judge-worker` service applies Trust Layer adjudication rules to submitted content. In this Phase 1 scaffold it runs as a minimal polling loop to confirm the container lifecycle works correctly. Trust Judge logic is a Phase 2 deliverable.

---

## Files

| Path | Purpose |
|---|---|
| `services/judge-worker/worker.py` | Service entrypoint; logs a startup message then loops indefinitely, sleeping 10 seconds between iterations |

### `services/judge-worker/worker.py`

```python
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main():
    logger.info("judge-worker: starting up")
    # Phase 2: Trust Judge logic will replace this loop
    while True:
        logger.info("judge-worker: running")
        time.sleep(10)


if __name__ == "__main__":
    main()
```

---

## Shared Dockerfile

`judge-worker` does **not** have its own Dockerfile. It reuses `services/api/Dockerfile` (Python 3.12-slim) and overrides the start command in `docker-compose.yml`:

```yaml
command: python worker.py
```

This keeps all Python dependency management in a single place. The `services/api/` source tree is also bind-mounted into the worker container at `/app`, so `worker.py` is available to the Python process.

Any change to `services/api/requirements.txt` applies to both services.

---

## Running locally

```bash
make up     # builds the shared image and starts all services
make ps     # confirm judge-worker is running
make logs   # tail logs; look for "judge-worker: running" lines
```

The service depends on `db` reaching a healthy state before it starts:

```yaml
depends_on:
  db:
    condition: service_healthy
```

To restart the worker without touching other services:

```bash
docker compose restart judge-worker
```

---

## Health check

The health check confirms the process is alive using `pgrep`:

```yaml
test: ["CMD-SHELL", "pgrep -f worker.py || exit 1"]
```

---

## Environment variables

| Variable | Default (`.env.example`) | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql://trustlayer:changeme@db:5432/trustlayer` | PostgreSQL connection string; available for Phase 2 use |

All variables are loaded from `.env` via the `env_file` directive in `docker-compose.yml`.
