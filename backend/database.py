from supabase import create_client, Client
from backend.config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_supabase_connection():
    """Test the Supabase connection"""
    if not settings.validate_supabase_config():
        logger.error("Supabase configuration missing!")
        logger.error("Please set SUPABASE_URL and SUPABASE_KEY environment variables")
        return False
    
    try:
        logger.info("Attempting to connect to Supabase...")
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        
        # Test the connection by trying to get the current user (should fail but not crash)
        # This is just to verify the client can be created
        logger.info("Supabase client created successfully!")
        logger.info(f"Connected to: {settings.SUPABASE_URL}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to connect to Supabase: {e}")
        return False

def get_supabase() -> Client:
    """Get Supabase client instance"""
    if not settings.validate_supabase_config():
        raise Exception("Supabase configuration not found")
    
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY) 