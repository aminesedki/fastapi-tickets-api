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

## Lancer en mode développement
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
