from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models import UserProfileCreate, UserProfileResponse
from app.database import get_supabase
from app.services.auth_service import AuthService

router = APIRouter(prefix="/profiles", tags=["user profiles"])
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

@router.post("/", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_user_profile(
    profile_data: UserProfileCreate, 
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new user profile in the database.
    
    The user_id is automatically taken from the authenticated user.
    """
    try:
        supabase = get_supabase()
        
        # Use the authenticated user's ID instead of the one in the request
        profile_to_insert = {
            "user_id": current_user["user_id"],  # Real user ID from auth
            "display_name": profile_data.display_name
        }
        
        # Insert the profile into the database
        response = supabase.table('user_profiles').insert(profile_to_insert).execute()
        
        if response.data:
            created_profile = response.data[0]
            return UserProfileResponse(
                user_id=created_profile['user_id'],
                display_name=created_profile['display_name'],
                created_at=str(created_profile['created_at']),
                updated_at=str(created_profile['updated_at'])
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user profile"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user profile: {str(e)}"
        ) 