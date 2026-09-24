# RCS API

> REST API for sending, tracking and querying RCS (Rich Communication Services) messaging events.

**Python · FastAPI · PostgreSQL · SQLAlchemy · Alembic · JWT · Docker**

| | |
|---|---|
| **Type** | Messaging API / Integration service |
| **Focus** | RCS delivery, event tracking and API security |
| **Architecture** | REST API + persistence + external RCS provider |
| **Status** | Public technical project |

## Overview

RCS API provides a backend boundary for applications that need to send RCS messages and track their lifecycle without coupling client systems directly to a messaging provider.

The project demonstrates a conventional production-oriented Python API stack with authentication, persistence, migrations, validation and containerized execution.

## Architecture

```text
Client Application
       │
       ▼
   FastAPI API
       │
  Auth / Validation
       │
   ┌───┴──────────┐
   │              │
PostgreSQL     RCS Provider
   │              │
   └── Events / Status
```

## Capabilities

- Send RCS messages from templates.
- Query message events with filtering and pagination.
- Retrieve events by callback/message identifier.
- JWT and API-key authentication.
- PostgreSQL persistence through SQLAlchemy.
- Schema validation with Pydantic.
- Database migrations with Alembic.
- Docker-based local environment.
- Interactive OpenAPI documentation through Swagger UI and ReDoc.

## API surface

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/v1/rcs/send/` | Send an RCS message |
| `GET` | `/v1/rcs/events/` | Query messaging events |
| `GET` | `/v1/rcs/events/{callback_message_id}` | Retrieve a specific event |

Additional API details are available through `/docs` and `/redoc` when the application is running.

## Quick start

### Docker

```bash
git clone https://github.com/jdrpires/RCSEugen.git
cd RCSEugen
./start.sh
```

The API documentation is then available at:

```text
http://localhost:8000/docs
```

Stop the environment with:

```bash
./stop.sh
```

### Local Python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

createdb rcs_db
alembic upgrade head
python init_db.py
python run.py
```

## Project structure

```text
RCSEugen/
├── alembic/          # Database migrations
├── app/
│   ├── routers/      # API routes
│   ├── auth.py       # Authentication / authorization
│   ├── database.py   # Persistence configuration
│   ├── main.py       # FastAPI application
│   ├── models.py     # SQLAlchemy models
│   └── schemas.py    # Pydantic schemas
├── Dockerfile
├── docker-compose.yml
├── init_db.py
├── requirements.txt
├── run.py
├── start.sh
└── stop.sh
```

## Security notes

- Keep credentials and API keys in environment variables.
- Do not commit real provider tokens or production secrets.
- Example/test credentials should never be reused in production.
- Review CORS, token lifetime and database permissions before production deployment.

## Why this project is public

This repository is part of my public engineering portfolio and demonstrates API design, integration boundaries, persistence, authentication and containerized Python services.

---

**Jean Pires** · [GitHub](https://github.com/jdrpires) · [Portfolio](https://github.com/jdrpires/jdrpires)
