from fastapi import APIRouter, HTTPException
from backend.services.email_service import EmailService
from backend.config import settings

router = APIRouter(prefix="/emails", tags=["emails"])

@router.get("/test-sendgrid")
async def test_sendgrid_connection():
    """
    Test SendGrid connection by sending a test email
    """
    try:
        email_service = EmailService()
        
        # Test email address - CHANGE THIS TO YOUR ACTUAL EMAIL
        test_email = "nilanikhita@gmail.com"  # Replace with your real email
        
        # Test the SendGrid connection
        result = await email_service.test_connection(test_email)
        
        if result["success"]:
            return {
                "success": True,
                "message": "SendGrid connection test successful! Email sent to " + test_email,
                "details": result
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"SendGrid connection test failed: {result['message']}"
            )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"SendGrid connection test failed: {str(e)}"
        ) 