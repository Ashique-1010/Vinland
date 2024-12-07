# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database.session import engine
from app.models import user, post
from app.controllers import auth, post as post_controller

# Create database tables
user.Base.metadata.create_all(bind=engine)
post.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog Platform API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(post_controller.router, prefix="/api/posts", tags=["Posts"])