# Backend developer commands. The shape of these targets IS the contract a
# new contributor reads first — keep them short, fast, and obvious.

.PHONY: help install dev seed test lint fmt typecheck migrate db-up db-down clean

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk -F ':.*?## ' '{printf "%-12s %s\n", $$1, $$2}'

install: ## Install deps + pre-commit hooks
	uv sync
	cd .. && pre-commit install

db-up: ## Start the Postgres container
	docker-compose up -d db
	@echo "waiting for postgres..."
	@until docker compose exec -T db pg_isready -U ieee >/dev/null 2>&1; do sleep 0.5; done
	@echo "postgres ready."

db-down: ## Stop the Postgres container
	docker compose down

dev: db-up ## Run migrations + start API with reload
	uv run alembic upgrade head
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

seed: ## Insert demo data (idempotent)
	uv run python -m scripts.seed

test: ## Run pytest with coverage
	uv run pytest --cov

lint: ## Ruff check + mypy
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy app

fmt: ## Ruff format
	uv run ruff format .
	uv run ruff check . --fix

typecheck: ## mypy only
	uv run mypy app

migrate: ## Generate a new migration. Usage: make migrate m="add X to events"
	@if [ -z "$(m)" ]; then echo "Usage: make migrate m=\"message\""; exit 1; fi
	uv run alembic revision --autogenerate -m "$(m)"
	uv run alembic upgrade head

clean: ## Remove caches and build artifacts
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov __pycache__
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
