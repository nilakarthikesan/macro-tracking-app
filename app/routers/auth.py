from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models import UserSignupRequest, UserLoginRequest, UserResponse, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])
auth_service = AuthService()
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