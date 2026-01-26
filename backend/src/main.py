import asyncio
import atexit
import logging
import secrets
from typing import Optional

from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from pathlib import Path
import os
from contextlib import asynccontextmanager

# Import local modules
from .api.routers import auth, users, courses, chat, questions, statistics, flashcard, files
from .api.routers import notes
#from .api.routers import notifications
from .api.routers import search as search_router
from .api.schemas import user as user_schema
from .db import database
from .db.crud import users_crud
from .db.models import db_user as user_model
from .utils import auth

from .core.routines import update_stuck_courses
from .config.settings import SESSION_SECRET_KEY
from .core.lifespan import lifespan

import logging
logger = logging.getLogger(__name__)

# Create database tables with error handling
try:
    user_model.Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created/verified successfully")
except Exception as e:
    logger.warning(f"⚠️ Could not create database tables on startup: {e}")
    logger.warning("Tables will be created on first database access.")

# Create output directory for flashcard files
output_dir = Path("/tmp/anki_output") if os.path.exists("/tmp") else Path("./anki_output")
output_dir.mkdir(exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Call the lifespan handler from core/lifespan.py
    async with life_span_from_core(app):
        yield

# Create the main app instance
app = FastAPI(
    title="User Management API",
    description="API for managing users with authentication",
    version="1.0.0",
    lifespan=lifespan
)

# DEBUG MIDDLEWARE: Log every request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"DEBUG MIDDLEWARE: Incoming request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        print(f"ERROR MIDDLEWARE: Request crashed: {e}")
        raise e


app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
    same_site="none",  # Required for cross-domain OAuth (Vercel frontend, Render backend)
    https_only=True,   # Required when same_site="none"
)


# CORS Configuration
# Get frontend URL from environment variable or use defaults
frontend_url = os.getenv("FRONTEND_BASE_URL", "http://localhost:3000")

origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite dev server
    "http://localhost:8000",
    frontend_url,  # Production frontend URL from env
    "https://kaizer-zeta.vercel.app",  # Explicit Vercel URL
]

# Remove None values
origins = [origin for origin in origins if origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",  # Allow all Vercel preview deployments
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
# Include your existing routers under this api_router
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(files.router)
app.include_router(search.router)  # search_router -> search
app.include_router(statistics.router)
app.include_router(auth.api_router) # auth_router -> auth
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
