from fastapi import APIRouter
from app.database import test_supabase_connection, get_supabase

router = APIRouter(tags=["health & testing"])

@router.get("/")
async def root():
    """Root endpoint - just to test if FastAPI is working."""
    return {
        "message": "Hello! FastAPI is working!",
        "status": "success"
    }

@router.get("/health")
async def health_check():
    """Health check - tells us if the server is running."""
    return {
        "status": "healthy", 
        "message": "Server is running"
    }

@router.get("/test-db")
async def test_database():
    """Test the Supabase database connection"""
    try:
        success = test_supabase_connection()
        if success:
            return {
                "status": "success",
                "message": "✅ Database connection successful!",
                "database": "Supabase"
            }
        else:
            return {
                "status": "error",
                "message": "❌ Database connection failed!",
                "database": "Supabase"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"❌ Database test failed: {str(e)}",
            "database": "Supabase"
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
            "message": "✅ Successfully connected to user_profiles table!",
            "data": response.data,
            "count": len(response.data)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"❌ Failed to read from user_profiles table: {str(e)}"
        } 