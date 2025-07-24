from fastapi import APIRouter
from app.database import get_supabase

router = APIRouter(tags=["health & testing"])

@router.get("/health")
async def health_check():
    """Health check - tells us if the server is running."""
    return {
        "status": "healthy", 
        "message": "Server is running"
    }

@router.get("/test-table")
async def test_user_profiles_table():
    """Test reading from the user_profiles table"""
    try:
        supabase = get_supabase()
        
        # Try to read from the user_profiles table
        response = supabase.table('user_profiles').select('*').limit(1).execute()
        
        return {
            "status": "success",
            "message": "Successfully connected to user_profiles table!",
            "data": response.data,
            "count": len(response.data)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to read from user_profiles table: {str(e)}"
        } 