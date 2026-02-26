from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..api.deps import get_db
from ..services.user_service import create_user, follow_user

router = APIRouter(tags=["users"])


@router.post("/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user_route(payload: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.UserRead:
    return create_user(db, payload)


@router.get("/users", response_model=list[schemas.UserRead])
def list_users(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[schemas.UserRead]:
    return crud.list_users(db, limit=limit, offset=offset)


@router.post("/users/{user_id}/follow/{target_id}", response_model=schemas.FollowRead, status_code=status.HTTP_201_CREATED)
def follow_user_route(user_id: int, target_id: int, db: Session = Depends(get_db)) -> schemas.FollowRead:
    return follow_user(db, user_id, target_id)
