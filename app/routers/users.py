from fastapi import APIRouter, Depends, HTTPException
from ..models import UserUpdate
from ..auth import get_current_active_user
from ..crud import update_user, get_user_by_id

router = APIRouter(prefix="/users", tags=["users"])


@router.put("/profile", response_model=dict)
async def update_profile(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    """Update user profile information"""
    updated_user = await update_user(current_user["id"], user_update)
    if not updated_user:
        raise HTTPException(status_code=400, detail="Failed to update profile")
    
    return updated_user


@router.get("/profile", response_model=dict)
async def get_profile(current_user: dict = Depends(get_current_active_user)):
    """Get current user profile"""
    return current_user 