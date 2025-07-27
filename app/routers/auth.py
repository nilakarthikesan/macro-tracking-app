from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models import UserSignupRequest, UserLoginRequest, UserResponse, TokenResponse
from app.services.auth_service import AuthService
from app.services.email_service import EmailService
from app.models import PasswordResetRequest

router = APIRouter(prefix="/auth", tags=["authentication"])
auth_service = AuthService()
email_service = EmailService()
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to get current user from JWT token"""
    token = credentials.credentials
    result = await auth_service.get_current_user(token)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result["error"]
        )
    
    return result

@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignupRequest):
    """
    Create a new user account using Supabase Auth.
    
    This creates a real user in the auth.users table.
    """
    result = await auth_service.signup_user(user_data.email, user_data.password)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    # Send welcome email
    try:
        await email_service.send_welcome_email(user_data.email, user_data.email.split('@')[0])
    except Exception as e:
        # Don't fail signup if email fails
        print(f"Warning: Failed to send welcome email: {str(e)}")
    
    return TokenResponse(
        access_token="signup_successful",  # In real app, this would be the actual token
        token_type="bearer",
        user_id=result["user_id"],
        email=result["email"]
    )

@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLoginRequest):
    """
    Authenticate user and return access token.
    
    This verifies credentials against Supabase Auth.
    """
    result = await auth_service.login_user(user_data.email, user_data.password)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result["error"]
        )
    
    return TokenResponse(
        access_token=result["access_token"],
        token_type="bearer",
        user_id=result["user_id"],
        email=result["email"]
    )

@router.post("/password-reset")
async def request_password_reset(reset_data: PasswordResetRequest):
    """
    Request a password reset email.
    """
    try:
        # Generate a simple reset token (in production, use proper JWT)
        reset_token = f"reset_{reset_data.email}_{hash(reset_data.email)}"
        
        # Send password reset email
        result = await email_service.send_password_reset_email(reset_data.email, reset_token)
        
        if result["success"]:
            return {
                "success": True,
                "message": "Password reset email sent successfully"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to send password reset email: {result['message']}"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error requesting password reset: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current user information from JWT token.
    
    This verifies the token and returns real user data.
    """
    return UserResponse(
        id=current_user["user_id"],
        email=current_user["email"],
        message="Real user data from Supabase Auth"
    ) 