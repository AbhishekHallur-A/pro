# Social Media App (Instagram + Twitter Hybrid) – Starter

Production-oriented FastAPI starter with clean layering, JWT auth, Dockerized Postgres, and React learning UI.

## Project structure (clean architecture)

```text
src/app/
  api/        # dependencies (auth/db wiring)
  routers/    # HTTP route definitions
  services/   # business logic / use-cases
  models.py   # SQLAlchemy ORM models
  schemas.py  # Pydantic request/response schemas
  database.py # engine/session setup
  settings.py # environment config
  security.py # bcrypt + JWT helpers
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Run API:

```bash
uvicorn src.app.main:app --reload
```

## API docs

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API testing steps

1. Register

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"user@example.com","username":"user1","password":"secret123"}'
```

2. Login

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"user@example.com","password":"secret123"}'
```

3. Use token on protected route

```bash
curl http://127.0.0.1:8000/auth/me -H 'Authorization: Bearer <ACCESS_TOKEN>'
```

## Environment configuration

Settings are loaded from `.env` with `APP_` prefix:
- `APP_DATABASE_URL`
- `APP_ENABLE_SQL_ECHO`
- `APP_JWT_SECRET`
- `APP_JWT_ALGORITHM`
- `APP_JWT_EXP_MINUTES`

## PostgreSQL + Docker

```bash
cp .env.example .env
docker compose up --build
```

## Alembic migrations

```bash
alembic upgrade head
alembic revision --autogenerate -m "your change"
```

## Frontend

- Vanilla UI: `./scripts/preview_frontend.sh 8080`
- React UI: `python -m http.server 8090 --directory frontend-react`
