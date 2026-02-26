from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import crud, schemas


def create_user(db: Session, payload: schemas.UserCreate):
    try:
        return crud.create_user(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists") from None


def follow_user(db: Session, user_id: int, target_id: int):
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
