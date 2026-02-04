from sqlalchemy.orm import Session

from . import models, schemas


def create_user(db: Session, payload: schemas.UserCreate) -> models.User:
    user = models.User(email=payload.email, username=payload.username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_users(db: Session, limit: int, offset: int) -> list[models.User]:
    return (
        db.query(models.User)
        .order_by(models.User.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )


def get_user(db: Session, user_id: int) -> models.User | None:
    return db.get(models.User, user_id)


def create_post(db: Session, payload: schemas.PostCreate) -> models.Post:
    post = models.Post(author_id=payload.author_id, content=payload.content)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_post(db: Session, post_id: int) -> models.Post | None:
    return db.get(models.Post, post_id)


def list_posts(db: Session, limit: int, offset: int) -> list[models.Post]:
    return (
        db.query(models.Post)
        .order_by(models.Post.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )


def add_comment(db: Session, post_id: int, payload: schemas.CommentCreate) -> models.Comment:
    comment = models.Comment(
        post_id=post_id,
        author_id=payload.author_id,
        content=payload.content,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def add_like(db: Session, post_id: int, payload: schemas.LikeCreate) -> models.Like:
    like = models.Like(post_id=post_id, user_id=payload.user_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like


def get_like(db: Session, post_id: int, user_id: int) -> models.Like | None:
    return (
        db.query(models.Like)
        .filter(models.Like.post_id == post_id, models.Like.user_id == user_id)
        .first()
    )


def follow_user(db: Session, user_id: int, target_id: int) -> models.Follow:
    follow = models.Follow(follower_id=user_id, following_id=target_id)
    db.add(follow)
    db.commit()
    db.refresh(follow)
    return follow


def get_follow(db: Session, user_id: int, target_id: int) -> models.Follow | None:
    return (
        db.query(models.Follow)
        .filter(models.Follow.follower_id == user_id, models.Follow.following_id == target_id)
        .first()
    )
