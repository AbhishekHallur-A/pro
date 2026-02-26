from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from .database import engine
from .models import Base
from .routers import auth, health, posts, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Social Media App Starter", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(_: Request, __: IntegrityError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": "Database constraint violation"})


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(health.router)
