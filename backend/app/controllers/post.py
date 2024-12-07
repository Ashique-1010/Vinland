from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.dependencies import get_db, get_current_user
from app.schemas.post import Post, PostCreate, PostUpdate
from app.models.user import User
from app.services.post import (
    create_post,
    get_posts,
    get_post,
    update_post,
    delete_post,
    search_posts,
)

router = APIRouter()

@router.post("/", response_model=Post)
async def create_new_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_post(db, post, current_user.id)

@router.get("/", response_model=List[Post])
def read_posts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return get_posts(db, skip=skip, limit=limit)

@router.get("/search", response_model=List[Post])
def search_posts_endpoint(
    query: str,
    db: Session = Depends(get_db)
):
    return search_posts(db, query)

@router.get("/{post_id}", response_model=Post)
def read_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = get_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=Post)
def update_existing_post(
    post_id: int,
    post: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_post = get_post(db, post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if existing_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    return update_post(db, post_id, post)

@router.delete("/{post_id}")
def delete_existing_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_post = get_post(db, post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if existing_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    delete_post(db, post_id)
    return {"message": "Post deleted successfully"}