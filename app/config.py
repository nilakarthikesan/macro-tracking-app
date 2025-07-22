import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Supabase Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    @classmethod
    def validate_supabase_config(cls) -> bool:
        """Validate that Supabase configuration is present"""
        return bool(cls.SUPABASE_URL and cls.SUPABASE_KEY)

# Create settings instance
settings = Settings() 