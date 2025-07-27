import os
from typing import Dict, Any
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from app.config import settings

class EmailService:
    def __init__(self):
        self.sendgrid_api_key = settings.SENDGRID_API_KEY
        self.from_email = settings.FROM_EMAIL
        self.from_name = settings.FROM_NAME
        
        if not self.sendgrid_api_key:
            raise ValueError("SENDGRID_API_KEY environment variable is required")
        
        self.sg = SendGridAPIClient(api_key=self.sendgrid_api_key)
    
    async def send_welcome_email(self, user_email: str, user_name: str) -> Dict[str, Any]:
        """
        Send welcome email to new users
        """
        try:
            mail = Mail(
                from_email=Email(self.from_email, self.from_name),
                to_emails=To(user_email),
                subject="Welcome to Macro Tracking App!"
            )
            
            html_content = f"""
            <h2>Welcome to Macro Tracking App!</h2>
            <p>Hi {user_name},</p>
            <p>Thank you for joining Macro Tracking App! We're excited to help you reach your fitness goals.</p>
            <p>Get started by:</p>
            <ul>
                <li>Setting your macro goals</li>
                <li>Logging your first meal</li>
                <li>Tracking your daily progress</li>
            </ul>
            <p>Happy tracking!</p>
            <p>- The Macro Tracking Team</p>
            """
            
            mail.content = Content("text/html", html_content)
            
            response = self.sg.send(mail)
            
            return {
                "success": True,
                "message": "Welcome email sent successfully",
                "status_code": response.status_code,
                "message_id": response.headers.get('X-Message-Id')
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to send welcome email: {str(e)}",
                "error": str(e)
            }
    
    async def send_password_reset_email(self, user_email: str, reset_token: str) -> Dict[str, Any]:
        """
        Send password reset email
        """
        try:
            mail = Mail(
                from_email=Email(self.from_email, self.from_name),
                to_emails=To(user_email),
                subject="Password Reset - Macro Tracking App"
            )
            
            reset_url = f"http://localhost:3000/reset-password?token={reset_token}"
            
            html_content = f"""
            <h2>Password Reset Request</h2>
            <p>You requested a password reset for your Macro Tracking App account.</p>
            <p>Click the link below to reset your password:</p>
            <p><a href="{reset_url}">Reset Password</a></p>
            <p>If you didn't request this, please ignore this email.</p>
            <p>This link will expire in 1 hour.</p>
            <p>- The Macro Tracking Team</p>
            """
            
            mail.content = Content("text/html", html_content)
            
            response = self.sg.send(mail)
            
            return {
                "success": True,
                "message": "Password reset email sent successfully",
                "status_code": response.status_code,
                "message_id": response.headers.get('X-Message-Id')
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to send password reset email: {str(e)}",
                "error": str(e)
            }
    
    async def test_connection(self, test_email: str) -> Dict[str, Any]:
        """
        Test SendGrid connection by sending a simple email.
        """
        try:
            print(f"Testing SendGrid connection...")
            print(f"   API Key: {self.sendgrid_api_key[:10]}...")
            print(f"   From: {self.from_email}")
            print(f"   To: {test_email}")
            
            # Create a simple test email with correct Content syntax
            mail = Mail(
                from_email=Email(self.from_email, self.from_name),
                to_emails=To(test_email),
                subject="SendGrid Connection Test - Macro Tracking App"
            )
            
            # Add content separately
            mail.content = Content("text/plain", "This is a test email to verify SendGrid connection is working!")
            
            # Send the email
            response = self.sg.send(mail)
            
            print(f"Email sent successfully!")
            print(f"   Status Code: {response.status_code}")
            print(f"   Message ID: {response.headers.get('X-Message-Id', 'N/A')}")
            
            return {
                "success": True,
                "message": "SendGrid connection test successful",
                "status_code": response.status_code,
                "message_id": response.headers.get('X-Message-Id')
            }
            
        except Exception as e:
            print(f"SendGrid connection failed: {str(e)}")
            return {
                "success": False,
                "message": f"SendGrid connection failed: {str(e)}",
                "error": str(e)
            } 