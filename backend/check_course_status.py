"""Check course creation status and error messages."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.config.settings import SQLALCHEMY_DATABASE_URL

def check_course_status():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        # Get course ID from argument or use latest
        if len(sys.argv) > 1:
            course_id = int(sys.argv[1])
            query = text("""
                SELECT id, title, description, status, error_msg, created_at, session_id
                FROM courses 
                WHERE id = :course_id
            """)
            result = db.execute(query, {"course_id": course_id}).fetchone()
            courses = [result] if result else []
        else:
            query = text("""
                SELECT id, title, description, status, error_msg, created_at, session_id
                FROM courses 
                ORDER BY created_at DESC
                LIMIT 5
            """)
            courses = db.execute(query).fetchall()
        
        if not courses:
            print("\n⚠️  No courses found")
            return
        
        print("\n" + "="*80)
        print("COURSE STATUS REPORT")
        print("="*80 + "\n")
        
        for course in courses:
            course_id, title, description, status, error_msg, created_at, session_id = course
            
            print(f"📌 Course ID: {course_id}")
            print(f"   Title: {title}")
            print(f"   Description: {description[:100] if description else 'None'}...")
            print(f"   Status: {status}")
            print(f"   Created: {created_at}")
            print(f"   Session ID: {session_id}")
            
            if error_msg:
                print(f"\n   ❌ ERROR MESSAGE:")
                print(f"   {error_msg}")
            
            print("-"*80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_course_status()
