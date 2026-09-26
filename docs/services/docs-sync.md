# Docs-Sync Service

The `docs-sync` service monitors the `docs/` directory for file-change events and logs them. Built on a Python 3.12-alpine base to minimise image size, it uses the `watchdog` library to observe the bind-mounted `/docs` volume. It has no dependencies on other services and can be stopped or restarted independently. Actual synchronisation logic (e.g. pushing updates to an external knowledge base) is a Phase 2 deliverable.

---

## Files

| Path | Purpose |
|---|---|
| `services/docs-sync/Dockerfile` | Container image definition; installs `watchdog` from `requirements.txt` and launches `watcher.py` |
| `services/docs-sync/requirements.txt` | Python package list: `watchdog` |
| `services/docs-sync/watcher.py` | Service entrypoint; starts a watchdog observer on `/docs` and logs file-change events |

### `services/docs-sync/watcher.py`

```python
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

WATCH_PATH = "/docs"


def main():
    logger.info("docs-sync: starting file watcher on %s", WATCH_PATH)
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_PATH, recursive=True)
    observer.start()
    # Phase 2: sync logic will replace this stub
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
```

---

## Running locally

```bash
make up     # builds the docs-sync image and starts all services
make ps     # confirm docs-sync is running
make logs   # tail logs; create or edit any file under docs/ to see events appear
```

The `docs/` directory at the repository root is bind-mounted to `/docs` inside the container, and `services/docs-sync/` is bind-mounted to `/app`. Any edit to a file under `docs/` while the service is running will produce a log entry.

To restart docs-sync without affecting the rest of the stack:

```bash
docker compose restart docs-sync
```

---

## Health check

The health check confirms the process is alive using `pgrep`:

```yaml
test: ["CMD-SHELL", "pgrep -f watcher.py || exit 1"]
```

---

## Environment variables

This service has no environment variables in Phase 1. The watched path (`/docs`) is hardcoded in `watcher.py` as a module-level constant and can be promoted to an environment variable in Phase 2 if needed.
