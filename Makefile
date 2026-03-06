SHELL := /bin/bash

COMPOSE := docker compose
VENV := venv

# Detect OS for venv binaries
ifeq ($(OS),Windows_NT)
	BIN := $(VENV)/Scripts
	PYTHON := python
else
	BIN := $(VENV)/bin
	PYTHON := python3
endif

# ---------- LOCAL DEV ----------
.PHONY: venv install install-dev run-local test-local lint-local fmt-local

venv:
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@$(BIN)/python -m pip install --upgrade pip

install: venv
	@$(BIN)/pip install -r requirements.txt

install-dev: install
	@$(BIN)/pip install -r requirements.dev.txt

run-local: install-dev
	@$(BIN)/uvicorn app.main:app --reload

test-local: install-dev
	@$(BIN)/python -m pytest -q

lint-local: install-dev
	@$(BIN)/ruff check app tests

fmt-local: install-dev
	@$(BIN)/ruff format app tests

# ---------- DEV ----------
.PHONY: dev-build dev-up dev-down dev-logs dev-shell
dev-build:
	$(COMPOSE) --profile dev build

dev-up:
	$(COMPOSE) --profile dev up -d --build

dev-down:
	$(COMPOSE) --profile dev down

dev-logs:
	$(COMPOSE) --profile dev logs -f api-dev

dev-shell:
	$(COMPOSE) --profile dev exec api-dev sh


# ---------- PROD ----------
.PHONY: prod-build prod-up prod-down prod-logs prod-shell
prod-build:
	$(COMPOSE) --profile prod build

prod-up:
	$(COMPOSE) --profile prod up -d --build

prod-down:
	$(COMPOSE) --profile prod down

prod-logs:
	$(COMPOSE) --profile prod logs -f api-prod

prod-shell:
	$(COMPOSE) --profile prod exec api-prod sh


# ---------- QUALITY ----------
.PHONY: test lint fmt
test:
	$(COMPOSE) --profile dev run --rm api-dev pytest -q

lint:
	$(COMPOSE) --profile dev run --rm api-dev ruff check app tests

fmt:
	$(COMPOSE) --profile dev run --rm api-dev ruff format app tests


# ---------- CLEAN ----------
.PHONY: clean clean-hard
clean:
	$(COMPOSE) down --remove-orphans
	docker image prune -f
	docker builder prune -f

clean-hard:
	$(COMPOSE) down -v --remove-orphans
	docker system prune -af --volumes