from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .security import create_access_token, decode_access_token, verify_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Social Media App Starter", version="0.1.0")
security = HTTPBearer(auto_error=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> models.User:
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing authorization token")
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from None

    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.post("/auth/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.UserRead:
    try:
        return crud.create_user(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists") from None


@app.post("/auth/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)) -> schemas.TokenResponse:
    user = crud.get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session = crud.create_session(db, user.id)
    return schemas.TokenResponse(
        access_token=create_access_token(user.id),
        session_token=session.token,
    )


@app.get("/auth/me", response_model=schemas.UserRead)
def me(current_user: models.User = Depends(get_current_user)) -> schemas.UserRead:
    return current_user


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
