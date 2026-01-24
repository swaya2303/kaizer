import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..core.routines import update_stuck_courses

scheduler = AsyncIOScheduler()
logger = logging.getLogger(__name__)

async def start_scheduler_async():
    """Start scheduler in background without blocking server startup"""
    await asyncio.sleep(2)  # Give server time to bind to port first
    try:
        logger.info("Starting background scheduler...")
        scheduler.add_job(update_stuck_courses, 'interval', hours=1)
        scheduler.start()
        logger.info("✅ Scheduler started successfully")
    except Exception as e:
        logger.warning(f"⚠️ Scheduler failed to start: {str(e)}")
        logger.warning("Server will continue without background tasks")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle including startup and shutdown events."""
    logger.info("Starting application...")
    
    # Start scheduler in background - don't wait for it
    scheduler_task = asyncio.create_task(start_scheduler_async())
    
    try:
        yield  # Server binds to port and starts serving here
    finally:
        logger.info("Shutting down application...")
        
        # Try to cancel scheduler startup if still running
        if not scheduler_task.done():
            scheduler_task.cancel()
        
        # Shutdown scheduler if it started
        if scheduler.running:
            try:
                scheduler.shutdown()
                logger.info("Scheduler stopped.")
            except Exception as e:
                logger.error(f"Error stopping scheduler: {e}")
        
        logger.info("Application shutdown complete.")
