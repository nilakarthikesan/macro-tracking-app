import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Supabase Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

    # JWT Configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App Configuration
    APP_NAME: str = "Macro Tracking App"
    APP_VERSION: str = "1.0.0"

    @classmethod
    def validate_supabase_config(cls) -> bool:
        """Validate that Supabase configuration is present"""
        return bool(cls.SUPABASE_URL and cls.SUPABASE_KEY)

# Create settings instance
settings = Settings()
