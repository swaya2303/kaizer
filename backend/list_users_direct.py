"""
List users using direct SQL to avoid model import issues.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.config.settings import SQLALCHEMY_DATABASE_URL

def list_users():
    """List all users using direct SQL."""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        query = text("""
            SELECT id, username, email, is_active, is_admin, created_at, last_login
            FROM users
            ORDER BY created_at DESC
        """)
        users = db.execute(query).fetchall()
        
        if not users:
            print("\n⚠️  No users found in the database.")
            print("You may need to create a user first.")
            return
        
        print(f"\n{'='*80}")
        print(f"DATABASE USERS ({len(users)} total)")
        print(f"{'='*80}\n")
        
        for i, user in enumerate(users, 1):
            user_id, username, email, is_active, is_admin, created_at, last_login = user
            
            status_icon = "✅" if is_active else "❌"
            admin_icon = "👑" if is_admin else "👤"
            
            print(f"{i}. {admin_icon} {username}")
            print(f"   ID: {user_id}")
            print(f"   Email: {email}")
            print(f"   Status: {status_icon} {'Active' if is_active else 'Inactive'}")
            print(f"   Admin: {'Yes' if is_admin else 'No'}")
            print(f"   Created: {created_at}")
            print(f"   Last Login: {last_login if last_login else 'Never'}")
            print(f"{'-'*80}")
        
        print(f"\n📊 Summary:")
        active_count = sum(1 for u in users if u[3])  # is_active
        admin_count = sum(1 for u in users if u[4])   # is_admin
        print(f"   Total users: {len(users)}")
        print(f"   Active users: {active_count}")
        print(f"   Admin users: {admin_count}")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    list_users()
