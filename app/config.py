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

    # SendGrid Configuration
    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY", "")
    FROM_EMAIL: str = os.getenv("FROM_EMAIL", "noreply@macro.works")
    FROM_NAME: str = os.getenv("FROM_NAME", "Macro Tracking App")

    # App Configuration
    APP_NAME: str = "Macro Tracking App"
    APP_VERSION: str = "1.0.0"

    @classmethod
    def validate_supabase_config(cls) -> bool:
        """Validate that Supabase configuration is present"""
        return bool(cls.SUPABASE_URL and cls.SUPABASE_KEY)

    @classmethod
    def validate_sendgrid_config(cls) -> bool:
        """Validate that SendGrid configuration is present"""
        return bool(cls.SENDGRID_API_KEY)

# Create settings instance
settings = Settings()
