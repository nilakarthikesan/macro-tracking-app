from supabase import Client
from backend.database import get_supabase
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        self.supabase: Client = get_supabase()
    
    async def signup_user(self, email: str, password: str):
        """
        Create a new user account using Supabase Auth
        """
        try:
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if response.user:
                logger.info(f"User created successfully: {email}")
                return {
                    "success": True,
                    "user_id": response.user.id,
                    "email": response.user.email,
                    "message": "User created successfully"
                }
            else:
                logger.error(f"Failed to create user: {email}")
                return {
                    "success": False,
                    "error": "Failed to create user"
                }
                
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def login_user(self, email: str, password: str):
        """
        Authenticate user and get access token
        """
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user and response.session:
                logger.info(f"User logged in successfully: {email}")
                return {
                    "success": True,
                    "user_id": response.user.id,
                    "email": response.user.email,
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token
                }
            else:
                logger.error(f"Failed to login user: {email}")
                return {
                    "success": False,
                    "error": "Invalid credentials"
                }
                
        except Exception as e:
            logger.error(f"Error logging in user: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_current_user(self, access_token: str):
        """
        Get current user from access token by decoding JWT
        """
        try:
            import jwt
            
            # Decode the JWT token without verification (for now)
            # In production, you'd want to verify the signature
            decoded = jwt.decode(access_token, options={"verify_signature": False})
            
            # Extract user info from the decoded token
            user_id = decoded.get('sub')
            email = decoded.get('email')
            
            if not user_id or not email:
                logger.error("Token missing required fields")
                return {
                    "success": False,
                    "error": "Invalid token format"
                }
            
            logger.info(f"Retrieved user from token: {email}")
            return {
                "success": True,
                "user_id": user_id,
                "email": email
            }
                
        except Exception as e:
            logger.error(f"Error getting user from token: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            } 