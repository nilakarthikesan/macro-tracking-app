from fastapi import APIRouter
from backend.database import get_supabase
from backend.services.email_service import EmailService

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

@router.post("/test-sendgrid")
async def test_sendgrid_connection(test_email: str):
    """Test SendGrid connection by sending a test email"""
    try:
        email_service = EmailService()
        result = await email_service.test_connection(test_email)
        
        return {
            "status": "success" if result["success"] else "error",
            "message": result["message"],
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to test SendGrid connection: {str(e)}"
        } 