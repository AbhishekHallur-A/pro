from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..api.deps import get_db
from ..services.post_service import add_comment, add_like, create_post

router = APIRouter(tags=["posts"])


@router.post("/posts", response_model=schemas.PostRead, status_code=status.HTTP_201_CREATED)
def create_post_route(payload: schemas.PostCreate, db: Session = Depends(get_db)) -> schemas.PostRead:
    return create_post(db, payload)


@router.get("/posts", response_model=list[schemas.PostRead])
def list_posts(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[schemas.PostRead]:
    return crud.list_posts(db, limit=limit, offset=offset)


@router.post("/posts/{post_id}/comments", response_model=schemas.CommentRead, status_code=status.HTTP_201_CREATED)
def add_comment_route(post_id: int, payload: schemas.CommentCreate, db: Session = Depends(get_db)) -> schemas.CommentRead:
    return add_comment(db, post_id, payload)


@router.post("/posts/{post_id}/likes", response_model=schemas.LikeRead, status_code=status.HTTP_201_CREATED)
def add_like_route(post_id: int, payload: schemas.LikeCreate, db: Session = Depends(get_db)) -> schemas.LikeRead:
    return add_like(db, post_id, payload)
