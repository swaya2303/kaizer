"""
List all users in the database for debugging purposes.
"""
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.db.models.db_user import User

def list_all_users():
    """List all users in the database."""
    
    db: Session = SessionLocal()
    
    try:
        users = db.query(User).all()
        
        if not users:
            print("No users found in the database.")
            return
        
        print(f"\nFound {len(users)} user(s) in the database:\n")
        print("="*80)
        
        for i, user in enumerate(users, 1):
            print(f"{i}. User ID: {user.id}")
            print(f"   Username: {user.username}")
            print(f"   Email: {user.email}")
            print(f"   Active: {'✅ Yes' if user.is_active else '❌ No'}")
            print(f"   Admin: {'✅ Yes' if user.is_admin else '❌ No'}")
            print(f"   Created: {user.created_at}")
            print(f"   Last Login: {user.last_login if user.last_login else 'Never'}")
            print(f"   Hash starts with: {user.hashed_password[:20]}...")
            print("-"*80)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    list_all_users()
