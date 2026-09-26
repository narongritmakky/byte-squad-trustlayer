# API Service

The `api` service is a FastAPI application that serves as the primary HTTP entry point for the TrustLayer platform. It is built from a Python 3.12-slim base image and exposes port `8000`.

---

## Files

| Path | Purpose |
|---|---|
| `services/api/Dockerfile` | Container image definition; installs Python dependencies and launches uvicorn |
| `services/api/requirements.txt` | Python package list: `fastapi`, `uvicorn[standard]`, `psycopg2-binary` |
| `services/api/app/__init__.py` | Empty file; makes `app/` a Python package importable by uvicorn |
| `services/api/app/main.py` | FastAPI application object; exposes the `/healthz` liveness endpoint |

### `services/api/app/main.py`

```python
from fastapi import FastAPI

app = FastAPI(title="TrustLayer API")


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
```

This is the only route in the Phase 1 scaffold. Business logic and additional routes are Phase 2 deliverables.

---

## Running locally

```bash
make up     # builds the image and starts all services
make ps     # confirm api is healthy
make logs   # tail logs from all services (Ctrl-C to stop)
```

The source tree at `services/api/` is bind-mounted into `/app` inside the container. `uvicorn` is started with `--reload`, so any file change is picked up automatically without rebuilding the image.

Once running, the health endpoint is reachable at:

```
http://localhost:8000/healthz
```

Expected response:

```json
{"status": "ok"}
```

---

## Health check

Docker Compose polls `GET /healthz` after the container starts:

```yaml
test: ["CMD-SHELL", "curl -f http://localhost:8000/healthz || exit 1"]
interval: 15s
timeout: 5s
retries: 3
start_period: 10s
```

Dependent services (`judge-worker`) will not start until this check passes.

---

## Environment variables

| Variable | Default (`.env.example`) | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql://trustlayer:changeme@db:5432/trustlayer` | PostgreSQL connection string; available for Phase 2 use |

All variables are loaded from `.env` via the `env_file` directive in `docker-compose.yml`. Copy `.env.example` to `.env` before running:

```bash
cp .env.example .env
```
