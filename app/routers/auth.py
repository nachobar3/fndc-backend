from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..models import UserCreate, Token, PasswordReset, PasswordResetConfirm, EmailVerification
from ..auth import create_access_token, get_current_user, get_password_hash
from ..crud import create_user, authenticate_user, get_user_by_email, verify_user_email, update_user_password
from ..email_service import email_service
from ..config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=dict)
async def register(user: UserCreate):
    """Register a new user and send verification email"""
    try:
        created_user = await create_user(user)
        
        # Send verification email
        await email_service.send_verification_email(user.email, user.name)
        
        return {
            "message": "User registered successfully. Please check your email to verify your account.",
            "user_id": created_user["id"]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user and return access token"""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.get("is_verified", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please verify your email before logging in"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/verify-email")
async def verify_email(verification: EmailVerification):
    """Verify user email with token"""
    email = email_service.verify_token(verification.token, "verification")
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")
    
    success = await verify_user_email(email)
    if not success:
        raise HTTPException(status_code=400, detail="User not found")
    
    return {"message": "Email verified successfully"}


@router.post("/forgot-password")
async def forgot_password(password_reset: PasswordReset):
    """Send password reset email"""
    user = await get_user_by_email(password_reset.email)
    if not user:
        # Don't reveal if email exists or not
        return {"message": "If the email exists, a password reset link has been sent"}
    
    success = await email_service.send_password_reset_email(password_reset.email, user["name"])
    if success:
        return {"message": "Password reset email sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send password reset email")


@router.post("/reset-password")
async def reset_password(reset_confirm: PasswordResetConfirm):
    """Reset password with token"""
    email = email_service.verify_token(reset_confirm.token, "password_reset")
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    success = await update_user_password(email, reset_confirm.new_password)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update password")
    
    return {"message": "Password reset successfully"}


@router.get("/me", response_model=dict)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return current_user 