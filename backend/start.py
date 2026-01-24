#!/usr/bin/env python3
"""
Production startup script for Render deployment with error handling
"""
import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_required_env_vars():
    """Check if required environment variables are set"""
    required_vars = [
        'SECRET_KEY',
        'DB_HOST',
        'DB_USER',
        'DB_PASSWORD',
        'DB_NAME'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these in your Render environment variables")
        return False
    
    logger.info("✅ All required environment variables are set")
    return True

def main():
    """Main startup function with error handling"""
    try:
        # Check environment variables
        if not check_required_env_vars():
            logger.error("Exiting due to missing environment variables")
            sys.exit(1)
        
        # Get port from environment
        port = int(os.getenv("PORT", 8000))
        logger.info(f"🚀 Starting server on 0.0.0.0:{port}")
        
        # Log database connection info (without password)
        logger.info(f"Database: {os.getenv('DB_USER')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME')}")
        
        # Import uvicorn here to catch import errors
        import uvicorn
        
        # Start uvicorn
        uvicorn.run(
            "src.main:app",
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True,
            timeout_keep_alive=30
        )
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        logger.error("Make sure all dependencies are installed")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        logger.exception("Full traceback:")
        sys.exit(1)

if __name__ == "__main__":
    main()
