from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
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
    try:
        return crud.create_user(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists") from None


@app.get("/users", response_model=list[schemas.UserRead])
def list_users(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[schemas.UserRead]:
    return crud.list_users(db, limit=limit, offset=offset)


@app.post("/posts", response_model=schemas.PostRead, status_code=status.HTTP_201_CREATED)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db)) -> schemas.PostRead:
    if not crud.get_user(db, payload.author_id):
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_post(db, payload)


@app.get("/posts", response_model=list[schemas.PostRead])
def list_posts(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[schemas.PostRead]:
    return crud.list_posts(db, limit=limit, offset=offset)


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
    if not crud.get_post(db, post_id):
        raise HTTPException(status_code=404, detail="Post not found")
    if not crud.get_user(db, payload.author_id):
        raise HTTPException(status_code=404, detail="Author not found")
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
    if not crud.get_post(db, post_id):
        raise HTTPException(status_code=404, detail="Post not found")
    if not crud.get_user(db, payload.user_id):
        raise HTTPException(status_code=404, detail="User not found")
    if crud.get_like(db, post_id, payload.user_id):
        raise HTTPException(status_code=400, detail="Post already liked")
    try:
        return crud.add_like(db, post_id, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Post already liked") from None


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
    if user_id == target_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    if not crud.get_user(db, user_id) or not crud.get_user(db, target_id):
        raise HTTPException(status_code=404, detail="User not found")
    if crud.get_follow(db, user_id, target_id):
        raise HTTPException(status_code=400, detail="Already following")
    try:
        return crud.follow_user(db, user_id, target_id)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Already following") from None


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
