"""
Diagnostic script to test user authentication and password hashing.
Run this to debug login issues.
"""
import sys
from sqlalchemy.orm import Session
from src.db.database import SessionLocal, engine
from src.db.models.db_user import User
from src.core.security import verify_password, get_password_hash

def test_user_login():
    """Test user authentication with diagnostic information."""
    
    db: Session = SessionLocal()
    
    try:
        # Get username/email and password from command line or use defaults
        if len(sys.argv) >= 3:
            username_or_email = sys.argv[1]
            password = sys.argv[2]
        else:
            print("Usage: python test_login.py <username_or_email> <password>")
            print("\nAlternatively, enter credentials below:")
            username_or_email = input("Enter username or email: ").strip()
            password = input("Enter password: ").strip()
        
        print("\n" + "="*60)
        print("AUTHENTICATION DIAGNOSTIC REPORT")
        print("="*60)
        
        # Search by username
        print(f"\n1. Searching for user by username: '{username_or_email}'")
        user = db.query(User).filter(User.username == username_or_email).first()
        
        # If not found, search by email
        if not user:
            print(f"   ❌ Not found by username")
            print(f"\n2. Searching for user by email: '{username_or_email}'")
            user = db.query(User).filter(User.email == username_or_email).first()
            
            if not user:
                print(f"   ❌ Not found by email")
                print("\n⚠️  USER NOT FOUND IN DATABASE")
                print("\nPossible solutions:")
                print("  - Check if the username/email is spelled correctly")
                print("  - Verify the user was created successfully")
                print("  - Run: python list_users.py to see all users")
                return
            else:
                print(f"   ✅ Found user by email")
        else:
            print(f"   ✅ Found user by username")
        
        # Display user information
        print(f"\n3. User Information:")
        print(f"   - ID: {user.id}")
        print(f"   - Username: {user.username}")
        print(f"   - Email: {user.email}")
        print(f"   - Is Active: {user.is_active}")
        print(f"   - Is Admin: {user.is_admin}")
        print(f"   - Hashed Password (first 50 chars): {user.hashed_password[:50]}...")
        print(f"   - Hash length: {len(user.hashed_password)} characters")
        
        # Check if user is active
        if not user.is_active:
            print("\n⚠️  USER IS INACTIVE")
            print("   The account exists but is disabled.")
            return
        
        # Test password verification
        print(f"\n4. Testing Password Verification:")
        print(f"   - Password entered: '{password}'")
        print(f"   - Password length: {len(password)} characters")
        
        # Verify password
        is_valid = verify_password(password, user.hashed_password)
        
        if is_valid:
            print(f"   ✅ PASSWORD VERIFICATION SUCCESSFUL!")
            print("\n✅ Authentication would succeed - login should work!")
        else:
            print(f"   ❌ PASSWORD VERIFICATION FAILED")
            print("\n❌ Authentication failed - password does not match")
            print("\nPossible causes:")
            print("  - Password is incorrect")
            print("  - Password contains hidden whitespace")
            print("  - Password was hashed incorrectly when user was created")
            print("  - Database password was manually modified")
            
            # Test if the stored hash is valid bcrypt
            if user.hashed_password.startswith('$2b$') or user.hashed_password.startswith('$2a$'):
                print("\n   Hash format looks like valid bcrypt ✅")
            else:
                print("\n   ⚠️  Hash doesn't look like bcrypt format!")
                print("   Expected to start with '$2b$' or '$2a$'")
                
            # Offer to generate a new hash
            print("\n5. Password Hash Test:")
            new_hash = get_password_hash(password)
            print(f"   - New hash for this password would be:")
            print(f"     {new_hash[:50]}...")
            print(f"\n   Would you like to update this user's password? (y/n): ", end="")
            response = input().strip().lower()
            
            if response == 'y':
                user.hashed_password = new_hash
                db.commit()
                print("   ✅ Password has been updated! Try logging in again.")
            else:
                print("   Password not updated.")
        
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_user_login()
