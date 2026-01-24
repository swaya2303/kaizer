"""
Reset passwords for test users in the database.
This makes it easy to set known passwords for MVP testing.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.config.settings import SQLALCHEMY_DATABASE_URL
from src.core.security import get_password_hash

def reset_all_passwords():
    """Reset passwords for all users to a known value."""
    
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        # Default password for all users
        default_password = "test123"
        
        print("="*70)
        print("PASSWORD RESET UTILITY FOR MVP TESTING")
        print("="*70)
        print("\nThis will reset ALL user passwords to a simple test password.")
        print("\n⚠️  WARNING: Only use this for local development/testing!")
        
        # Get custom password if provided
        if len(sys.argv) > 1:
            default_password = sys.argv[1]
            print(f"\nUsing custom password: {default_password}")
        else:
            print(f"\nDefault password will be: {default_password}")
            print("\nTo use a different password, run:")
            print("  python reset_passwords.py <your_password>")
        
        print("\nPress Enter to continue, or Ctrl+C to cancel...")
        input()
        
        # Get all users
        users_query = text("SELECT id, username, email FROM users")
        users = db.execute(users_query).fetchall()
        
        if not users:
            print("\n⚠️  No users found in database!")
            return
        
        # Hash the password once
        hashed_password = get_password_hash(default_password)
        
        print(f"\n📝 Resetting passwords for {len(users)} user(s)...")
        print("-"*70)
        
        # Update each user
        update_query = text("UPDATE users SET hashed_password = :hash WHERE id = :user_id")
        
        for user_id, username, email in users:
            db.execute(update_query, {"hash": hashed_password, "user_id": user_id})
            print(f"✅ Reset password for: {username} ({email})")
        
        db.commit()
        
        print("-"*70)
        print(f"\n✅ SUCCESS! All passwords have been reset.")
        print(f"\n📋 Login credentials for all users:")
        print(f"   Password: {default_password}")
        print("\n   Users:")
        for user_id, username, email in users:
            print(f"   - Username: {username}")
        
        print("\n💡 You can now login with any username and the password above.")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_all_passwords()
