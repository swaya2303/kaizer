"""
Script to initialize the database tables and create a user
"""
import mysql.connector
from passlib.context import CryptContext
import uuid

# Password hashing
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Database connection config
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'wayam@2303',
    'database': 'nexora_db'
}

# SQL to create tables
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    profile_image_base64 LONGTEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME DEFAULT CURRENT_TIMESTAMP,
    login_streak INT DEFAULT 0,
    is_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(100),
    is_subscribed BOOLEAN DEFAULT FALSE,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

CREATE_COURSES_TABLE = """
CREATE TABLE IF NOT EXISTS courses (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    language VARCHAR(10) DEFAULT 'en',
    status VARCHAR(20) DEFAULT 'draft',
    image_base64 LONGTEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

CREATE_CHAPTERS_TABLE = """
CREATE TABLE IF NOT EXISTS chapters (
    id VARCHAR(50) PRIMARY KEY,
    course_id VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    content LONGTEXT,
    order_index INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    INDEX idx_course_id (course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

def main():
    print("🔄 Connecting to MySQL...")
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Create tables
        print("📦 Creating users table...")
        cursor.execute(CREATE_USERS_TABLE)
        
        print("📦 Creating courses table...")
        cursor.execute(CREATE_COURSES_TABLE)
        
        print("📦 Creating chapters table...")
        cursor.execute(CREATE_CHAPTERS_TABLE)
        
        conn.commit()
        print("✅ Tables created successfully!")
        
        # Create user
        print("\n👤 Creating user 'swayam'...")
        user_id = str(uuid.uuid4())
        username = 'swayam'
        email = 'swayamanand09@gmail.com'
        password = 'swayam2303'
        hashed_password = pwd_context.hash(password)
        
        sql = """
        INSERT INTO users (id, username, email, hashed_password, is_active, is_admin, is_verified, login_streak)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (user_id, username, email, hashed_password, True, False, True, 0)
        cursor.execute(sql, values)
        conn.commit()
        
        print("✅ User created successfully!")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        
        # Verify
        cursor.execute("SELECT username, email FROM users")
        users = cursor.fetchall()
        print(f"\n📋 Users in database: {users}")
        
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        print("\n🔌 Database connection closed.")

if __name__ == "__main__":
    main()
