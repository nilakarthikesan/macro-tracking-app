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

@router.get("/me", response_model=UserProfileResponse)
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Get the current user's profile from the database.
    """
    try:
        supabase = get_supabase()
        
        # Query for the user's profile using their user_id
        response = supabase.table('user_profiles').select('*').eq('user_id', current_user["user_id"]).execute()
        
        if response.data:
            profile = response.data[0]
            return UserProfileResponse(
                user_id=profile['user_id'],
                display_name=profile['display_name'],
                created_at=str(profile['created_at']),
                updated_at=str(profile['updated_at'])
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user profile: {str(e)}"
        )

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

@router.put("/me", response_model=UserProfileResponse)
async def update_user_profile(
    profile_data: UserProfileCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update the current user's profile in the database.
    """
    try:
        supabase = get_supabase()
        
        # Prepare the update data
        update_data = {}
        if profile_data.display_name is not None:
            update_data["display_name"] = profile_data.display_name
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        # Update the profile in the database
        response = supabase.table('user_profiles').update(update_data).eq('user_id', current_user["user_id"]).execute()
        
        if response.data:
            updated_profile = response.data[0]
            return UserProfileResponse(
                user_id=updated_profile['user_id'],
                display_name=updated_profile['display_name'],
                created_at=str(updated_profile['created_at']),
                updated_at=str(updated_profile['updated_at'])
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user profile: {str(e)}"
        )

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Delete the current user's profile from the database.
    """
    try:
        supabase = get_supabase()
        
        # Delete the profile from the database
        response = supabase.table('user_profiles').delete().eq('user_id', current_user["user_id"]).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user profile: {str(e)}"
        ) 