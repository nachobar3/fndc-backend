from fastapi import APIRouter, Depends, HTTPException
from ..models import UserUpdate, UserRole
from ..auth import get_current_active_user, get_current_admin_user
from ..crud import update_user, get_user_by_id, get_all_users, update_user_role

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


# Admin endpoints
@router.get("/", response_model=list)
async def get_all_users_admin(current_admin: dict = Depends(get_current_admin_user)):
    """Get all users (admin only)"""
    users = await get_all_users()
    return users


@router.put("/{user_id}/role", response_model=dict)
async def update_user_role_admin(
    user_id: str,
    role: UserRole,
    current_admin: dict = Depends(get_current_admin_user)
):
    """Update user role (admin only)"""
    # Verificar que el usuario existe
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # No permitir cambiar el rol del propio admin
    if user_id == current_admin["id"]:
        raise HTTPException(status_code=400, detail="Cannot change your own role")
    
    success = await update_user_role(user_id, role)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update user role")
    
    return {
        "message": "User role updated successfully",
        "user_id": user_id,
        "new_role": role
    } 