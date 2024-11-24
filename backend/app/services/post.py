from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from app.services.ml_service import ContentModerationService, moderation_service
from fastapi import HTTPException
import logging

content_preprocessor = moderation_service._preprocess
content_censor = moderation_service.is_content_allowed
async def create_post(db: Session, post: PostCreate, author_id: int):
    # Check for offensive content
    processed_content = content_preprocessor(post.content)
    if not await content_censor(processed_content):
        raise HTTPException(
            status_code=400,
            detail="Post contains offensive content and cannot be published"
        )
    
    db_post = Post(
        title=post.title,
        content=post.content,
        tags=post.tags,
        author_id=author_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

async def update_post(db: Session, post_id: int, post: PostUpdate):
    db_post = get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    # Check for offensive content
    processed_content = content_preprocessor(post.content)
    if not await content_censor(processed_content):
        raise HTTPException(
            status_code=400,
            detail="Post contains offensive content and cannot be published"
        )
    
    for var, value in vars(post).items():
        setattr(db_post, var, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post

async def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(db_post)
    db.commit()
    return True

def search_posts(db: Session, query: str):
    return db.query(Post).filter(
        or_(
            Post.title.ilike(f"%{query}%"),
            Post.content.ilike(f"%{query}%"),
            Post.tags.ilike(f"%{query}%")
        )
    ).all()