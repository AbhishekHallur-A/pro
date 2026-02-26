from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..api.deps import get_current_user, get_db
from ..services.auth_service import login_user, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserRead)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.UserRead:
    return register_user(db, payload)


@router.post("/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)) -> schemas.TokenResponse:
    return login_user(db, payload)


@router.get("/me", response_model=schemas.UserRead)
def me(current_user=Depends(get_current_user)) -> schemas.UserRead:
    return current_user
