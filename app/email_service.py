import resend
from .config import settings
from datetime import datetime, timedelta, UTC
import jwt


class EmailService:
    def __init__(self):
        resend.api_key = settings.RESEND_API_KEY
    
    def create_verification_token(self, email: str) -> str:
        """Create a verification token for email verification"""
        payload = {
            "email": email,
            "type": "verification",
            "exp": datetime.now(UTC) + timedelta(hours=24)
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    def create_password_reset_token(self, email: str) -> str:
        """Create a password reset token"""
        payload = {
            "email": email,
            "type": "password_reset",
            "exp": datetime.now(UTC) + timedelta(hours=1)
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    def verify_token(self, token: str, token_type: str):
        """Verify a token and return the email"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            if payload.get("type") != token_type:
                return None
            return payload.get("email")
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    async def send_verification_email(self, email: str, name: str):
        """Send verification email to user"""
        token = self.create_verification_token(email)
        verification_url = f"http://localhost:8000/verify-email?token={token}"
        
        html_content = f"""
        <html>
            <body>
                <h2>Bienvenido a FNDC Tournament System</h2>
                <p>Hola {name},</p>
                <p>Gracias por registrarte. Por favor verifica tu cuenta haciendo clic en el siguiente enlace:</p>
                <a href="{verification_url}" style="background-color: #4CAF50; color: white; padding: 14px 20px; text-decoration: none; border-radius: 4px;">
                    Verificar Email
                </a>
                <p>Este enlace expirará en 24 horas.</p>
                <p>Si no creaste esta cuenta, puedes ignorar este email.</p>
            </body>
        </html>
        """
        
        try:
            resend.Emails.send({
                "from": "noreply@fndc.com",
                "to": [email],
                "subject": "Verifica tu cuenta - FNDC Tournament System",
                "html": html_content
            })
            return True
        except Exception as e:
            print(f"Error sending verification email: {e}")
            return False
    
    async def send_password_reset_email(self, email: str, name: str):
        """Send password reset email to user"""
        token = self.create_password_reset_token(email)
        reset_url = f"http://localhost:8000/reset-password?token={token}"
        
        html_content = f"""
        <html>
            <body>
                <h2>Recuperación de Contraseña</h2>
                <p>Hola {name},</p>
                <p>Has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace para crear una nueva contraseña:</p>
                <a href="{reset_url}" style="background-color: #4CAF50; color: white; padding: 14px 20px; text-decoration: none; border-radius: 4px;">
                    Restablecer Contraseña
                </a>
                <p>Este enlace expirará en 1 hora.</p>
                <p>Si no solicitaste este cambio, puedes ignorar este email.</p>
            </body>
        </html>
        """
        
        try:
            resend.Emails.send({
                "from": "noreply@fndc.com",
                "to": [email],
                "subject": "Recuperación de Contraseña - FNDC Tournament System",
                "html": html_content
            })
            return True
        except Exception as e:
            print(f"Error sending password reset email: {e}")
            return False


email_service = EmailService() 