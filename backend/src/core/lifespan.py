import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..core.routines import update_stuck_courses

scheduler = AsyncIOScheduler()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle including startup and shutdown events."""
    logger.info("Starting application...")
    
    scheduler_started = False
    try:
        # Try to start scheduler, but don't block server startup if it fails
        scheduler.add_job(update_stuck_courses, 'interval', hours=1)
        scheduler.start()
        scheduler_started = True
        logger.info("✅ Scheduler started successfully")   
    except Exception as e:
        logger.warning(f"⚠️ Scheduler failed to start: {str(e)}")
        logger.warning("Server will continue without background tasks")
        # Don't raise - let the server start anyway
    
    try:
        yield  # Server runs here
    finally:
        logger.info("Shutting down application...")
        if scheduler_started and scheduler.running:
            try:
                scheduler.shutdown()
                logger.info("Scheduler stopped.")
            except Exception as e:
                logger.error(f"Error stopping scheduler: {e}")
        logger.info("Application shutdown complete.")
