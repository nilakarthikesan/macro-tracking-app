from fastapi import APIRouter, HTTPException, status
from app.models import UserProfileCreate, UserProfileResponse
from app.database import get_supabase

router = APIRouter(prefix="/profiles", tags=["user profiles"])

@router.post("/", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_user_profile(profile_data: UserProfileCreate):
    """Create a new user profile in the database"""
    try:
        supabase = get_supabase()
        
        # Prepare the data to insert
        profile_to_insert = {
            "user_id": profile_data.user_id,
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