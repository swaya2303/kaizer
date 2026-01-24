import os
import sys
from pathlib import Path

# Check various paths
backend_dir = Path(__file__).parent
env_file = backend_dir / ".env"

print(f"Current directory: {os.getcwd()}")
print(f"Backend directory: {backend_dir}")
print(f".env file path: {env_file}")
print(f".env exists: {env_file.exists()}")

if env_file.exists():
    print(f"\n.env file size: {env_file.stat().st_size} bytes")
    
    # Read and check for API key
    with open(env_file, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            if 'GOOGLE_API_KEY' in line:
                # Show line number and first 50 chars
                print(f"Line {i}: {line.strip()[:60]}...")
                
                # Check if it has actual value
                if '=' in line:
                    key, value = line.split('=', 1)
                    value = value.strip()
                    if value and value != 'your_api_key_here':
                        print(f"✅ API key is set (length: {len(value)})")
                        print(f"✅ Starts with: {value[:10]}")
                    else:
                        print(f"❌ API key is placeholder or empty")
  
# Now test load_dotenv
print(f"\n--- Testing load_dotenv() ---")
from dotenv import load_dotenv
load_result = load_dotenv(env_file)
print(f"load_dotenv() returned: {load_result}")

api_key = os.getenv('GOOGLE_API_KEY')
print(f"GOOGLE_API_KEY after load_dotenv: {api_key[:20] if api_key else 'NOT SET'}...")
