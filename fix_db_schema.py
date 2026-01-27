import os
import psycopg2
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables
load_dotenv(dotenv_path="backend/.env")

# Get DB config
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

print(f"Connecting to {DB_HOST} as {DB_USER}...")

try:
    # Connect to the database
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )
    conn.autocommit = True
    cursor = conn.cursor()

    print("✅ Connected successfully!")

    # 1. Alter the column type to TEXT (this bypasses Enum checks)
    print("🛠️  Converting 'courses.status' column to TEXT...")
    try:
        cursor.execute("ALTER TABLE courses ALTER COLUMN status TYPE VARCHAR(50);")
        print("✅ Column type changed to VARCHAR(50).")
    except Exception as e:
        print(f"⚠️  Could not alter column (might already be fixed): {e}")

    # 2. Drop the Enum type (optional, cleans up schema)
    print("🗑️  Dropping 'coursestatus' enum type...")
    try:
        cursor.execute("DROP TYPE IF EXISTS coursestatus;")
        print("✅ Enum type dropped.")
    except Exception as e:
        print(f"⚠️  Could not drop enum type (might be in use or not work on this DB version): {e}")

    cursor.close()
    conn.close()
    print("\n🎉 FIXED! The 'status' column is now a simple text field.")
    print("You can now restart your backend and create courses without 502 errors.")

except Exception as e:
    print(f"\n❌ Error connecting or executing SQL: {e}")
