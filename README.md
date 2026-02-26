# Social Media App (Instagram + Twitter Hybrid) – Starter

This starter includes:
- FastAPI backend API (`src/app`)
- Browser-based Web UI (`frontend/`)
- Local containerized deployment with Postgres (`Dockerfile`, `docker-compose.yml`)

## Quick start (local Python)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.app.main:app --reload
```

## Environment variable management

1. Copy the example file:

```bash
cp .env.example .env
```

2. Update values for your environment (`APP_JWT_SECRET` is required for production).

Current app settings are read from `.env` using `APP_` prefix:
- `APP_DATABASE_URL`
- `APP_ENABLE_SQL_ECHO`
- `APP_JWT_SECRET`
- `APP_JWT_ALGORITHM`
- `APP_JWT_EXP_MINUTES`

## Docker deployment (API + Postgres)

```bash
cp .env.example .env
docker compose up --build
```

API will be available at `http://localhost:8000` and Postgres at `localhost:5432`.

## Frontend preview

```bash
./scripts/preview_frontend.sh 8080
```

Then open `http://localhost:8080` and point API base URL to `http://127.0.0.1:8000`.

## API

- `POST /auth/register` register with email, username, password
- `POST /auth/login` login and receive JWT access token + session token
- `GET /auth/me` read current user from Bearer token
- `POST /users` create a user
- `GET /users` list users
- `POST /posts` create a post
- `GET /posts` list posts
- `POST /posts/{post_id}/comments` add comment
- `POST /posts/{post_id}/likes` like a post
- `POST /users/{user_id}/follow/{target_id}` follow a user
- `GET /health` health check


## Phase 2 — React frontend (best for learning)

A React-based UI is available in `frontend-react/` (CDN + Babel for zero-build learning setup). It is designed with a cleaner, intuitive layout, consistent styling, responsive behavior, and immediate feedback states for loading/success/errors.

Run it locally:

```bash
python -m http.server 8090 --directory frontend-react
```

Then open `http://localhost:8090`.
