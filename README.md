# Social Media App (Instagram + Twitter Hybrid) - Starter

This is a minimal, production-oriented starter codebase for a social media app. It implements core entities (users, posts, comments, likes, follows) using FastAPI and SQLAlchemy, and is designed to evolve into a scalable service.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.app.main:app --reload
```

## API

- `POST /users` create a user
- `GET /users` list users
- `POST /posts` create a post
- `GET /posts` list posts
- `POST /posts/{post_id}/comments` add comment
- `POST /posts/{post_id}/likes` like a post
- `POST /users/{user_id}/follow/{target_id}` follow a user

## Notes
- Uses SQLite for development. Set `APP_DATABASE_URL` for Postgres in production.
- This starter focuses on the core domain model to keep the initial scaffold clean and extensible.
