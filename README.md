# CRUD API Tickets

API REST développée avec FastAPI, SQLAlchemy Async et SQLite.
Déploiement via Docker avec gestion simplifiée par Makefile.

---

## Stack Technique

-   Python 3.12
-   FastAPI
-   SQLAlchemy 2 (Async)
-   SQLite
-   Docker & Docker Compose
-   Pytest
-   Ruff (linting)
-   Logging structuré


## Installation
git clone https://github.com/aminesedki/fastapi-tickets-api.git
cd fastapi-tickets-api

## Prérequis
Avant de lancer le projet, vérifiez que les outils nécessaires sont installés :

docker -v

docker compose version

make --version

## Structure du projet

```bash
.
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── domain/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── modules/
│   ├── tests/
│   ├── utils/
│   ├── logs/
│   ├── pyproject.toml
│   ├── .env
│   └── main.py
│
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── README.md
├── .gitignore
└── LICENSE
```

## Lancer en mode développement locale

make run-local

make test-local

make lint-local


## Lancer en mode docker compose
make dev-up

## Mode production
make prod-up

## Arrêter l’application
make dev-down

ou

make prod-down

## Tests
make test

## Qualité de Code
Lint: make lint

Formatage: make fmt

## Nettoyage Docker
make clean

## Nettoyage Docker complet
make clean-hard

**Note:** la commande supprime volumes et images inutilisées !


## Endpoints

url : http://localhost:8080/

Base URL : /api/v1/tickets

Swagger: /docs

GET /api/v1/tickets

GET /api/v1/tickets/{id}

POST /api/v1/tickets

PUT /api/v1/tickets/{id}

PATCH /api/v1/tickets/{id}

DELETE /api/v1/tickets/{id}

## Environnements

L’environnement actif est affiché :

-   Dans Swagger (TICKETS API (DEV) ou (PROD))

-   Sur la page d’accueil '/'

Variables d’environnement importantes :

-   ENV

-   API_VERSION

-   DATABASE_URL

-   LOG_LEVEL



## License
MIT License
