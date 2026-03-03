COMPOSE := docker compose

# ---------- DEV ----------
.PHONY: dev-up dev-build  dev-down
dev-build:
	$(COMPOSE) --profile dev build

dev-up:
	$(COMPOSE) --profile dev up -d --build

dev-down:
	$(COMPOSE) down


# ---------- PROD ----------
.PHONY: prod-build prod-up prod-logs prod-down prod-shell
prod-build:
	$(COMPOSE) --profile prod build

prod-up:
	$(COMPOSE) --profile prod up -d --build

prod-down:
	$(COMPOSE) down


# ---------- QUALITY ----------
.PHONY: test lint fmt
test:
	$(COMPOSE) --profile dev run --rm api-dev pytest -q

lint:
	$(COMPOSE) --profile dev run --rm api-dev ruff check .

fmt:
	$(COMPOSE) --profile dev run --rm api-dev ruff format .


# ---------- CLEAN ----------
.PHONY: clean clean-hard
clean:
	$(COMPOSE) down --remove-orphans
	docker image prune -f
	docker builder prune -f

clean-hard:
	$(COMPOSE) down -v --remove-orphans
	docker system prune -af --volumes