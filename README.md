# Social Media App (Instagram + Twitter Hybrid) – Starter

This starter now includes both:
- A FastAPI backend API (`src/app`)
- A browser-based Web UI (`frontend/`) that calls the live API

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.app.main:app --reload
```

In another terminal, start the UI preview:

```bash
./scripts/preview_frontend.sh 8080
```

Then open `http://localhost:8080` and use the API box (top-right) to point to your backend (default `http://127.0.0.1:8000`).

## API

- `POST /users` create a user
- `GET /users` list users
- `POST /posts` create a post
- `GET /posts` list posts
- `POST /posts/{post_id}/comments` add comment
- `POST /posts/{post_id}/likes` like a post
- `POST /users/{user_id}/follow/{target_id}` follow a user
- `GET /health` health check
