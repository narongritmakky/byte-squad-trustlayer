SHELL := /bin/bash
COMPOSE_FILE ?= docker-compose.yml

.PHONY: up down destroy restart logs ps test-infra help

up: ## Start all services (build if needed)
	docker compose -f $(COMPOSE_FILE) up -d --build

down: ## Stop containers (volumes are preserved)
	docker compose -f $(COMPOSE_FILE) down

destroy: ## Remove containers AND named volumes (full reset)
	docker compose -f $(COMPOSE_FILE) down -v

restart: ## Restart all services without rebuilding
	docker compose -f $(COMPOSE_FILE) restart

logs: ## Show recent logs for all services (use make logs ARGS=--follow to tail)
	docker compose -f $(COMPOSE_FILE) logs $(ARGS)

ps: ## Show status of all services
	docker compose -f $(COMPOSE_FILE) ps

test-infra: ## Run all infrastructure validation scripts (stops on first failure)
	bash tests/infra/test_containers_start.sh && bash tests/infra/test_volume_persistence.sh && bash tests/infra/test_makefile_commands.sh

help: ## List all available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
