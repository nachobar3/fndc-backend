import os
from google.auth.transport import requests
from google.oauth2 import id_token
from google.auth.exceptions import GoogleAuthError
from app.config import settings


class GoogleAuthService:
    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
    
    async def verify_google_token(self, token: str) -> dict:
        """
        Verify Google ID token and return user information
        """
        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                self.client_id
            )
            
            # Extract user information
            user_info = {
                "email": idinfo["email"],
                "name": idinfo.get("name", ""),
                "picture": idinfo.get("picture", ""),
                "google_id": idinfo["sub"],
                "email_verified": idinfo.get("email_verified", False)
            }
            
            return user_info
            
        except GoogleAuthError as e:
            raise ValueError(f"Invalid Google token: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error verifying Google token: {str(e)}")


# Create a global instance
google_auth_service = GoogleAuthService() 