import sys
sys.path.insert(0, '.')
from sqlalchemy import create_engine, text
from src.config.settings import SQLALCHEMY_DATABASE_URL

conn = create_engine(SQLALCHEMY_DATABASE_URL).connect()
result = conn.execute(text("SELECT id, status FROM courses WHERE id=5")).fetchone()
print(f"Course {result[0]}: {result[1]}")

# Get error if exists  
err = conn.execute(text("SELECT error_msg FROM courses WHERE id=5")).fetchone()
if err[0]:
    print(f"\n=== ERROR MESSAGE ===")
    print(err[0][:500])
else:
    print("\nNo error message - task may still be running or silently failing")
    
conn.close()
