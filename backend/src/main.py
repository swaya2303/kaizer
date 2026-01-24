import asyncio
import atexit
import logging
import secrets
from typing import Optional

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from pathlib import Path
import os

from .api.routers import auth as auth_router
from .api.routers import courses, files, users, statistics, questions
from .api.routers import notes
#from .api.routers import notifications
from .api.routers import chat
from .api.routers import search as search_router
from .api.routers import flashcard
from .api.schemas import user as user_schema
from .db.database import engine, SessionLocal
from .db.models import db_user as user_model
from .utils import auth

from .core.routines import update_stuck_courses
from .config.settings import SESSION_SECRET_KEY
from .core.lifespan import lifespan

import logging
logger = logging.getLogger(__name__)

# Create database tables with error handling
# COMMENTED OUT: This was blocking server startup on Render
# Tables will be created lazily on first database access
# try:
#     user_model.Base.metadata.create_all(bind=engine)
#     logger.info("✅ Database tables created/verified successfully")
# except Exception as e:
#     logger.warning(f"⚠️ Could not create database tables on startup: {e}")
#     logger.warning("This is normal if database is not yet accessible. Tables will be created on first connection.")

# Create output directory for flashcard files
output_dir = Path("/tmp/anki_output") if os.path.exists("/tmp") else Path("./anki_output")
output_dir.mkdir(exist_ok=True)

# Create the main app instance
app = FastAPI(
    title="User Management API",
    root_path="/api",
    lifespan=lifespan  # Use the lifespan context manager
)


app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY
)


# CORS Configuration
# Get frontend URL from environment variable or use defaults
frontend_url = os.getenv("FRONTEND_BASE_URL", "http://localhost:3000")

origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite dev server
    "http://localhost:8000",
    frontend_url,  # Production frontend URL from env
    "https://*.vercel.app",  # Allow all Vercel preview deployments
]

# Remove None values and add wildcard support
origins = [origin for origin in origins if origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now - you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define /users/me BEFORE including users.router to ensure correct route matching
@app.get("/users/me", response_model=Optional[user_schema.User], tags=["users"])
async def read_users_me(current_user: Optional[user_model.User] = Depends(auth.get_current_user_optional)):
    """Get the current logged-in user's details."""
    return current_user

# Include your existing routers under this api_router
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(files.router)
app.include_router(search_router.router)  # Add search router
app.include_router(statistics.router)
app.include_router(auth_router.api_router)
app.include_router(notes.router)
#app.include_router(notifications.router)
app.include_router(questions.router)
app.include_router(chat.router)
app.include_router(flashcard.router)

# Mount static files for flashcard downloads
app.mount("/output", StaticFiles(directory=str(output_dir)), name="output")


# The root path "/" is now outside the /api prefix
@app.get("/")
async def root():
    """Status endpoint for the API."""
    return {"message": "Welcome to the User Management API. API endpoints are under /api"}
