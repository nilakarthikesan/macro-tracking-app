from fastapi import APIRouter, status
from app.models import UserSignupRequest, UserLoginRequest, UserResponse, TokenResponse

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignupRequest):
    """
    Create a new user account.
    
    This is a dummy implementation for Phase 1.
    Later we'll add actual database storage.
    """
    # For now, just return a dummy response
    # In Phase 2, we'll actually save to database
    return TokenResponse(
        access_token="dummy_token_12345",
        token_type="bearer",
        user_id="user_123",
        email=user_data.email
    )

@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLoginRequest):
    """
    Authenticate user and return access token.
    
    This is a dummy implementation for Phase 1.
    Later we'll add actual password verification.
    """
    # For now, just return a dummy response
    # In Phase 2, we'll actually verify credentials
    return TokenResponse(
        access_token="dummy_token_12345",
        token_type="bearer",
        user_id="user_123",
        email=user_data.email
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user():
    """
    Get current user information.
    
    This is a dummy implementation for Phase 1.
    Later we'll add JWT token verification.
    """
    # For now, just return dummy user data
    # In Phase 2, we'll verify JWT token and get real user data
    return UserResponse(
        id="user_123",
        email="user@example.com",
        message="This is dummy user data for Phase 1"
    ) 