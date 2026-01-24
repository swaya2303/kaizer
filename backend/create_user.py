"""
Script to create a user in the database
"""
import mysql.connector
from passlib.context import CryptContext
import uuid

# Password hashing
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# User details
username = 'swayam'
email = 'swayamanand09@gmail.com'
password = 'swayam2303'
hashed_password = pwd_context.hash(password)
user_id = str(uuid.uuid4())

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='wayam@2303',  # Your MySQL password from .env
    database='nexora_db'
)

cursor = conn.cursor()

try:
    # Insert user
    sql = """
    INSERT INTO users (id, username, email, hashed_password, is_active, is_admin, is_verified, login_streak, created_at, last_login)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
    """
    values = (user_id, username, email, hashed_password, True, False, True, 0)
    cursor.execute(sql, values)
    conn.commit()
    
    print("✅ User created successfully!")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"   ID: {user_id}")
    
except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
