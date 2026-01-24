import sys
sys.path.insert(0, '.')
from sqlalchemy import create_engine, text
from src.config.settings import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
conn = engine.connect()
result = conn.execute(text("SELECT id, title, status, LENGTH(COALESCE(error_msg, '')) as error_len FROM courses WHERE id IN (1,2,3) ORDER BY id DESC")).fetchall()

print("\n=== COURSE STATUS ===")
for row in result:
    print(f"\nCourse ID: {row[0]}")
    print(f"Title: {row[1]}")
    print(f"Status: {row[2]}")
    print(f"Has Error: {'Yes' if row[3] > 0 else 'No'}")

# Get full error for latest course
latest = conn.execute(text("SELECT id, error_msg FROM courses WHERE id=3")).fetchone()
if latest and latest[1]:
    print(f"\n=== ERROR FOR COURSE {latest[0]} ===")
    print(latest[1][:500])  # First 500 chars

conn.close()
