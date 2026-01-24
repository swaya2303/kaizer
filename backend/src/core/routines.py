"""
Core routines
"""
import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..db.database import get_db
from ..db.models.db_course import Course, CourseStatus  # Your SQLAlchemy model


def update_stuck_courses():
    """
    Check for courses that are stuck in 'creating' status for more than 2 hours
    and mark them as 'error'.
    """
    logging.info("Checking for stuck courses...")
    
    try:
        db_gen = get_db()
        db: Session = next(db_gen)
    except Exception as e:
        logging.error("Failed to connect to database in scheduler: %s", e)
        logging.warning("Skipping stuck course check - database not available")
        return  # Exit gracefully if DB is not available

    try:
        threshold = datetime.now(timezone.utc) - timedelta(hours=2) # 2 hours threshold

        stuck_courses = db.query(Course).filter(
            Course.status == "creating",
            Course.created_at < threshold
        ).all()

        for course in stuck_courses:
            logging.info("Marking course %s as error due to timeout.", course.id)

            course.status = CourseStatus.FAILED
            course.error_msg = "Course creation timed out."
        db.commit()
        logging.info("Marked %s stuck courses as error.", len(stuck_courses))

    except SQLAlchemyError as e:
        logging.error("Scheduler error: %s", e)
        db.rollback()
    except Exception as e:
        logging.error("Unexpected error in scheduler: %s", e)
    finally:
        try:
            next(db_gen, None)
        except:
            pass  # Ignore cleanup errors

