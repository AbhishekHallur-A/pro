from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Social Media App Starter", version="0.1.0")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.UserRead:
    return crud.create_user(db, payload)


@app.get("/users", response_model=list[schemas.UserRead])
def list_users(db: Session = Depends(get_db)) -> list[schemas.UserRead]:
    return crud.list_users(db)


@app.post("/posts", response_model=schemas.PostRead, status_code=status.HTTP_201_CREATED)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db)) -> schemas.PostRead:
    return crud.create_post(db, payload)


@app.get("/posts", response_model=list[schemas.PostRead])
def list_posts(db: Session = Depends(get_db)) -> list[schemas.PostRead]:
    return crud.list_posts(db)


@app.post(
    "/posts/{post_id}/comments",
    response_model=schemas.CommentRead,
    status_code=status.HTTP_201_CREATED,
)
def add_comment(
    post_id: int,
    payload: schemas.CommentCreate,
    db: Session = Depends(get_db),
) -> schemas.CommentRead:
    if not db.get(models.Post, post_id):
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.add_comment(db, post_id, payload)


@app.post(
    "/posts/{post_id}/likes",
    response_model=schemas.LikeRead,
    status_code=status.HTTP_201_CREATED,
)
def add_like(
    post_id: int,
    payload: schemas.LikeCreate,
    db: Session = Depends(get_db),
) -> schemas.LikeRead:
    if not db.get(models.Post, post_id):
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.add_like(db, post_id, payload)


@app.post(
    "/users/{user_id}/follow/{target_id}",
    response_model=schemas.FollowRead,
    status_code=status.HTTP_201_CREATED,
)
def follow_user(
    user_id: int,
    target_id: int,
    db: Session = Depends(get_db),
) -> schemas.FollowRead:
    if not db.get(models.User, user_id) or not db.get(models.User, target_id):
        raise HTTPException(status_code=404, detail="User not found")
    return crud.follow_user(db, user_id, target_id)
