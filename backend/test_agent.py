"""
Simple test to verify the background task is working.
We'll manually trigger a minimal course creation to see if agents respond.
"""
import asyncio
import sys
sys.path.insert(0, '.')

from src.services.agent_service import AgentService
from src.api.schemas.course import CourseRequest

async def test_agent():
    """Test if agents can run at all."""
    print("\n" + "="*70)
    print("TESTING AGENT SERVICE")
    print("="*70 + "\n")
    
    try:
        agent_service = AgentService()
        print("✅ AgentService initialized")
        
        # Try to run info agent with minimal input
        print("\nTesting InfoAgent...")
        result = await agent_service.info_agent.run(
            user_id="test_user",
            state={},
            content={"text": "Test document about Python programming"}
        )
        
        print(f"✅ InfoAgent returned: {result}")
        print("\n" + "="*70)
        print("SUCCESS - Agents are working!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_agent())
    sys.exit(0 if success else 1)
