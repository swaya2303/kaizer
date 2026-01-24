"""
Simple diagnostic script to check user authentication using direct SQL.
This avoids SQLAlchemy model relationship issues.
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.config.settings import SQLALCHEMY_DATABASE_URL
from src.core.security import verify_password, get_password_hash

def test_login_direct():
    """Test user login using direct SQL queries."""
    
    # Create engine and session
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        # Get credentials
        if len(sys.argv) >= 3:
            username_or_email = sys.argv[1]
            password = sys.argv[2]
        else:
            print("Usage: python test_login_direct.py <username_or_email> <password>")
            print("\nAlternatively, enter credentials below:")
            username_or_email = input("Enter username or email: ").strip()
            password = input("Enter password: ").strip()
        
        print("\n" + "="*70)
        print("AUTHENTICATION DIAGNOSTIC REPORT")
        print("="*70)
        
        # Search for user by username
        print(f"\n1. Searching for user: '{username_or_email}'")
        query = text("""
            SELECT id, username, email, is_active, is_admin, hashed_password, created_at, last_login
            FROM users 
            WHERE username = :identifier OR email = :identifier
            LIMIT 1
        """)
        result = db.execute(query, {"identifier": username_or_email}).fetchone()
        
        if not result:
            print(f"   ❌ USER NOT FOUND")
            print("\n⚠️  No user exists with that username or email")
            print("\nTrying to list all users...")
            
            # List all users
            all_users = db.execute(text("SELECT username, email FROM users LIMIT 10")).fetchall()
            if all_users:
                print(f"\nExisting users in database:")
                for user in all_users:
                    print(f"   - Username: {user[0]}, Email: {user[1]}")
            else:
                print("\n⚠️  No users found in database!")
            return
        
        # Unpack user data
        user_id, username, email, is_active, is_admin, hashed_password, created_at, last_login = result
        
        print(f"   ✅ User found!")
        print(f"\n2. User Information:")
        print(f"   - ID: {user_id}")
        print(f"   - Username: {username}")
        print(f"   - Email: {email}")
        print(f"   - Is Active: {is_active}")
        print(f"   - Is Admin: {is_admin}")
        print(f"   - Created: {created_at}")
        print(f"   - Last Login: {last_login if last_login else 'Never'}")
        print(f"   - Hash (first 50 chars): {hashed_password[:50]}...")
        print(f"   - Hash length: {len(hashed_password)} characters")
        
        # Check if active
        if not is_active:
            print("\n⚠️  USER IS INACTIVE - Login will fail")
            return
        
        # Test password
        print(f"\n3. Password Verification Test:")
        print(f"   - Testing password: '{password}'")
        print(f"   - Password length: {len(password)} chars")
        
        is_valid = verify_password(password, hashed_password)
        
        if is_valid:
            print(f"   ✅ PASSWORD IS CORRECT!")
            print("\n✅✅✅ AUTHENTICATION SUCCESSFUL ✅✅✅")
            print("\nLogin should work with these credentials.")
        else:
            print(f"   ❌ PASSWORD VERIFICATION FAILED")
            print("\n❌ Password does not match the stored hash")
            
            # Check hash format
            if hashed_password.startswith('$2b$') or hashed_password.startswith('$2a$'):
                print("\n   ℹ️  Hash format is valid bcrypt")
            else:
                print("\n   ⚠️  Hash format looks incorrect!")
                print(f"   Expected bcrypt hash starting with '$2b$' or '$2a$'")
                print(f"   Actual hash starts with: {hashed_password[:10]}")
            
            # Offer to reset password
            print("\n4. Password Reset Option:")
            print(f"   Would you like to reset the password for '{username}'? (y/n): ", end="")
            response = input().strip().lower()
            
            if response == 'y':
                new_hash = get_password_hash(password)
                update_query = text("UPDATE users SET hashed_password = :hash WHERE id = :user_id")
                db.execute(update_query, {"hash": new_hash, "user_id": user_id})
                db.commit()
                print("   ✅ Password has been reset! Try logging in again.")
            else:
                print("   Password not changed.")
        
        print("\n" + "="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_login_direct()
