"""Verify Google API key is loaded and test basic agent functionality."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_api_key():
    """Check if Google API key is configured."""
    print("\n" + "="*70)
    print("GOOGLE GEMINI API KEY CHECK")
    print("="*70 + "\n")
    
    # Check environment variable
    api_key_from_env = os.getenv("GOOGLE_API_KEY")
    
    print(f"1. Environment Variable Check:")
    if api_key_from_env:
        print(f"   ✅ GOOGLE_API_KEY is set")
        print(f"   Key starts with: {api_key_from_env[:10]}...")
        print(f"   Key length: {len(api_key_from_env)} characters")
    else:
        print(f"   ❌ GOOGLE_API_KEY is NOT set in environment")
        return False
    
    # Check settings module
    try:
        from src.config import settings
        print(f"\n2. Settings Module Check:")
        if hasattr(settings, 'GOOGLE_API_KEY') and settings.GOOGLE_API_KEY:
            print(f"   ✅ settings.GOOGLE_API_KEY is loaded")
            print(f"   Key starts with: {settings.GOOGLE_API_KEY[:10]}...")
        else:
            print(f"   ❌ settings.GOOGLE_API_KEY is NOT loaded")
            return False
    except Exception as e:
        print(f"   ❌ Error loading settings: {e}")
        return False
    
    # Try to initialize an agent
    print(f"\n3. Agent Initialization Test:")
    try:
        from google.adk.sessions import InMemorySessionService
        from src.agents.info_agent.agent import InfoAgent
        
        session_service = InMemorySessionService()
        info_agent = InfoAgent("TestApp", session_service)
        print(f"   ✅ InfoAgent initialized successfully")
        
    except Exception as e:
        print(f"   ❌ Failed to initialize agent: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print(f"\n" + "="*70)
    print(f"✅ ALL CHECKS PASSED - API key is configured correctly")
    print(f"="*70 + "\n")
    
    return True

if __name__ == "__main__":
    success = check_api_key()
    sys.exit(0 if success else 1)
