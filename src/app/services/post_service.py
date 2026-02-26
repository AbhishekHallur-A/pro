from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import crud, schemas


def create_post(db: Session, payload: schemas.PostCreate):
    if not crud.get_user(db, payload.author_id):
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_post(db, payload)


def add_comment(db: Session, post_id: int, payload: schemas.CommentCreate):
    if not crud.get_post(db, post_id):
        raise HTTPException(status_code=404, detail="Post not found")
    if not crud.get_user(db, payload.author_id):
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.add_comment(db, post_id, payload)


def add_like(db: Session, post_id: int, payload: schemas.LikeCreate):
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
