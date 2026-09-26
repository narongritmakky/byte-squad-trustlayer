# Makefile

The `Makefile` at the project root wraps the full Docker Compose lifecycle in
single-word targets so developers can operate the stack without memorising underlying
`docker compose` flags. Run `make help` at any time to see every available target and
its description.

---

## Variable: `COMPOSE_FILE`

```make
COMPOSE_FILE ?= docker-compose.yml
```

The `?=` operator means the variable is only set if it has not already been set in the
environment. This makes the Makefile overridable for CI pipelines without editing the
file itself:

```sh
# CI override — point at a test-specific compose file
COMPOSE_FILE=docker-compose.ci.yml make up
```

This is the only variable that needs to be overridden for most CI scenarios.

---

## Targets

### `up`

```sh
docker compose -f $(COMPOSE_FILE) up -d --build
```

Builds any images whose source files have changed since the last build, then starts all
services in detached mode. Safe to run repeatedly — containers that are already running
are not restarted unless their image changed.

---

### `down`

```sh
docker compose -f $(COMPOSE_FILE) down
```

Stops and removes containers and the default network. **Named volumes are not touched.**
The `pgdata` volume — and all PostgreSQL data inside it — survives this command. This is
intentional: the volume persistence test (`tests/infra/test_volume_persistence.sh`)
relies on `make down` preserving data so it can verify the row survives a full
stop/start cycle.

---

### `destroy`

```sh
docker compose -f $(COMPOSE_FILE) down -v
```

Stops and removes containers, the default network, **and all named volumes** (including
`pgdata`). Use this when you need a completely clean slate — for example, after a schema
migration that is incompatible with existing data, or to hand off a reproducible
environment to a colleague.

> **`down` vs `destroy` at a glance**
>
> | Command | Containers removed | `pgdata` volume removed |
> |---|:---:|:---:|
> | `make down` | ✓ | ✗ |
> | `make destroy` | ✓ | ✓ |

---

### `restart`

```sh
docker compose -f $(COMPOSE_FILE) restart
```

Sends a stop/start signal to every running container without rebuilding images. Useful
for picking up configuration changes (e.g. environment variable edits) that do not
require a new image build.

---

### `logs`

```sh
docker compose -f $(COMPOSE_FILE) logs -f
```

Tails the combined log stream for all services. Press `Ctrl+C` to stop following. To
tail a single service, call docker compose directly:

```sh
docker compose logs -f api
```

---

### `ps`

```sh
docker compose -f $(COMPOSE_FILE) ps
```

Prints a table of all services with their current state, health status, and exposed
ports. Handy for a quick sanity check after `make up`.

---

### `test-infra`

```sh
bash tests/infra/test_containers_start.sh && \
bash tests/infra/test_volume_persistence.sh && \
bash tests/infra/test_makefile_commands.sh
```

Runs the three infrastructure validation scripts in order. The `&&` chaining means
execution stops immediately on the first failure, so you always see the first broken
script rather than a cascade of errors from dependent scripts.

See [`docs/tests-infra.md`](tests-infra.md) for a description of what each script
checks.

---

### `help`

```sh
@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
```

Self-documenting target. Scans `$(MAKEFILE_LIST)` (the list of all included Makefiles)
for lines matching `target: ## description` and prints them in aligned, colour-coded
columns. Adding a new target with a `## comment` automatically makes it appear here —
no manual maintenance required.

---

## Adding a new target

1. Write the target with a `## <description>` comment on the same line as the rule:
   ```make
   migrate: ## Run database migrations
       docker compose exec api alembic upgrade head
   ```
2. Add the target name to `.PHONY`.
3. `make help` will pick it up automatically.
