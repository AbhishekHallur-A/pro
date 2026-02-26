from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..security import create_access_token, verify_password


def register_user(db: Session, payload: schemas.UserCreate) -> schemas.UserRead:
    try:
        return crud.create_user(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists") from None


def login_user(db: Session, payload: schemas.LoginRequest) -> schemas.TokenResponse:
    user = crud.get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session = crud.create_session(db, user.id)
    return schemas.TokenResponse(access_token=create_access_token(user.id), session_token=session.token)
